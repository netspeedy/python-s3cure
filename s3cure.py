#!/usr/bin/env python3
"""
MinIO Bucket Creator Script

This script creates a MinIO bucket with associated admin and service accounts.
It provides a command-line interface for creating S3-compatible storage resources
with appropriate access credentials and policies.
"""

import argparse
import json
import os
import secrets
import string
import subprocess
import sys
from typing import Dict, Tuple, Union

# Configuration Constants
DEFAULT_S3_ENDPOINT = "https://s3.netspeedy.io"
DEFAULT_ADMIN_USERNAME = "{bucket_name}"  # Will be formatted with bucket name

class MinIOBucketCreator:
    """
    A class to handle the creation of MinIO buckets and associated resources.

    This class manages the creation of MinIO buckets, admin users, policies,
    and service accounts with appropriate permissions.

    Attributes:
        bucket_name (str): Name of the MinIO bucket to create
        endpoint (str): S3 endpoint URL
        admin_username (str): Username for the admin account
        admin_policy_name (str): Name of the admin policy
    """

    def __init__(self, bucket_name: str, endpoint: str = DEFAULT_S3_ENDPOINT):
        """
        Initialize the MinIO bucket creator.

        Args:
            bucket_name (str): Name of the bucket to create
            endpoint (str): S3 endpoint URL, defaults to DEFAULT_S3_ENDPOINT
        """
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.admin_username = DEFAULT_ADMIN_USERNAME.format(bucket_name=bucket_name)
        self.admin_policy_name = f"{bucket_name}-admin-policy"

    def generate_random_string(self, length: int = 24) -> str:
        """
        Generate a random string for use as credentials.

        Args:
            length (int): Length of the string to generate, defaults to 24

        Returns:
            str: Random string containing letters and numbers
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def run_command(self, command: list) -> bool:
        """
        Execute a shell command and handle its output.

        Args:
            command (list): Command to execute as a list of strings

        Returns:
            bool: True if command succeeded, False otherwise
        """
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip()
            if "Your previous request to create the named bucket succeeded" in error_message:
                print(f"\n⚠️  Bucket '{self.bucket_name}' already exists.")
                sys.exit(2)  # Exit with code 2 for "bucket exists"
            else:
                print(f"\n❌ Error: {error_message}")
            return False

    def create_bucket(self) -> bool:
        """
        Create a new MinIO bucket.

        Returns:
            bool: True if bucket creation succeeded, False otherwise
        """
        return self.run_command(["mc", "mb", f"minio/{self.bucket_name}"])

    def create_admin_policy(self) -> bool:
        """
        Create an admin policy for the bucket.

        Returns:
            bool: True if policy creation succeeded, False otherwise
        """
        policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": ["s3:*"],
                "Resource": [
                    f"arn:aws:s3:::{self.bucket_name}/*",
                    f"arn:aws:s3:::{self.bucket_name}"
                ]
            }]
        }

        policy_file = f"{self.admin_policy_name}.json"
        try:
            with open(policy_file, 'w', encoding='utf-8') as f:
                json.dump(policy, f, indent=4)
            result = self.run_command([
                "mc", "admin", "policy", "create",
                "minio", self.admin_policy_name, policy_file
            ])
            os.remove(policy_file)
            return result
        except IOError as e:
            print(f"\n❌ Policy creation error: {str(e)}")
            return False

    def create_admin_user(self, admin_secret: str) -> bool:
        """
        Create an admin user for the bucket.

        Args:
            admin_secret (str): Password for the admin user

        Returns:
            bool: True if user creation succeeded, False otherwise
        """
        return self.run_command([
            "mc", "admin", "user", "add",
            "minio", self.admin_username, admin_secret
        ])

    def create_service_account(self) -> Union[Tuple[str, str], bool]:
        """
        Create a service account for the bucket.

        Returns:
            Union[Tuple[str, str], bool]: Tuple of (access_key, secret_key) if successful,
                                        False otherwise
        """
        try:
            result = subprocess.run(
                ["mc", "admin", "user", "svcacct", "add", "minio", self.admin_username],
                capture_output=True,
                text=True,
                check=True
            )

            access_key = ""
            secret_key = ""
            for line in result.stdout.splitlines():
                if "Access Key:" in line:
                    access_key = line.split(":")[1].strip()
                elif "Secret Key:" in line:
                    secret_key = line.split(":")[1].strip()

            if access_key and secret_key:
                return access_key, secret_key
            return False

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Service account creation error: {e.stderr}")
            return False

    def attach_policy(self) -> bool:
        """
        Attach the admin policy to the admin user.

        Returns:
            bool: True if policy attachment succeeded, False otherwise
        """
        return self.run_command([
            "mc", "admin", "policy", "attach",
            "minio", self.admin_policy_name, "--user", self.admin_username
        ])

    def setup_bucket(self) -> Dict:
        """
        Set up the complete bucket infrastructure.

        This method orchestrates the creation of all necessary resources:
        - MinIO bucket
        - Admin policy
        - Admin user
        - Service account

        Returns:
            Dict: Dictionary containing all created resource details
        """
        # Create bucket first - if it exists, the script will exit in run_command
        if not self.create_bucket():
            print("\n❌ Bucket creation failed. Exiting...")
            sys.exit(1)

        admin_secret = self.generate_random_string()

        # Create and setup admin user
        if not self.create_admin_policy():
            print("\n❌ Admin policy creation failed. Exiting...")
            sys.exit(1)

        if not self.create_admin_user(admin_secret):
            print("\n❌ Admin user creation failed. Exiting...")
            sys.exit(1)

        if not self.attach_policy():
            print("\n❌ Policy attachment failed. Exiting...")
            sys.exit(1)

        # Create service account
        svc_account_result = self.create_service_account()
        if not svc_account_result:
            print("\n❌ Service account creation failed. Exiting...")
            sys.exit(1)

        svc_access_key, svc_secret_key = svc_account_result

        return {
            "bucket": self.bucket_name,
            "endpoint": self.endpoint,
            "admin_user": {
                "username": self.admin_username,
                "secret_key": admin_secret
            },
            "service_account": {
                "access_key": svc_access_key,
                "secret_key": svc_secret_key
            }
        }

def main():
    """
    Main function to handle command-line interface and script execution.
    """
    parser = argparse.ArgumentParser(
        description='MinIO Bucket Creator - Create a bucket with admin and service accounts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Example:
  %(prog)s --bucket-name my-bucket
  %(prog)s -b my-bucket --endpoint https://custom-s3-endpoint.com
        '''
    )

    parser.add_argument('--bucket-name', '-b',
                       required=True,
                       help='Name of the bucket to create')

    parser.add_argument('--endpoint',
                       default=DEFAULT_S3_ENDPOINT,
                       help=f'S3 endpoint URL (default: {DEFAULT_S3_ENDPOINT})')

    args = parser.parse_args()

    creator = MinIOBucketCreator(args.bucket_name, args.endpoint)
    credentials = creator.setup_bucket()

    # Display credentials with new formatting
    print("\n🌟 MinIO Bucket Creator - Resource Details 🌟")
    print("=" * 60)
    print("\n🔑 Admin Credentials:")
    print(f"   • Username: {credentials['admin_user']['username']}")
    print(f"   • Password: {credentials['admin_user']['secret_key']}")
    print("\n🔐 Service Account Credentials:")
    print(f"   • Access Key: {credentials['service_account']['access_key']}")
    print(f"   • Secret Key: {credentials['service_account']['secret_key']}")
    print(f"   • Bucket: {credentials['bucket']}")
    print(f"   • Endpoint: {credentials['endpoint']}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
