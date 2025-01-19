# s3cure.py - MinIO Bucket Creator 🚀

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![MinIO](https://img.shields.io/badge/MinIO-Compatible-orange.svg)](https://min.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview 📋

`s3cure.py` is a Python-based automation tool designed to simplify the creation and management of MinIO buckets, admin accounts, service accounts, and policies. By leveraging the MinIO Client (`mc`), this tool provides a streamlined way to set up S3-compatible storage resources with secure credentials and policies, making it ideal for enterprise environments.

---

## Key Features ✨

- 🪣 **Automated MinIO bucket creation**  
  Quickly create MinIO buckets with a single command.
- 👤 **Admin account generation**  
  Securely generate admin accounts with random credentials.
- 🔒 **Custom policy creation**  
  Automatically create and attach policies for bucket access.
- 🔑 **Service account generation**  
  Generate service accounts with access and secret keys.
- 🛡️ **Security-first design**  
  Implements the principle of least privilege and uses cryptographically secure random credentials.

---

## Prerequisites 📋

Before using `s3cure.py`, ensure the following requirements are met:

1. **Python 3.6 or higher**  
   Install Python from [python.org](https://www.python.org/).

2. **MinIO Client (`mc`) installed and configured**  
   The script relies on the `mc` CLI tool to interact with the MinIO server. Install it from the [MinIO Client page](https://min.io/docs/minio/linux/reference/minio-mc.html).

3. **Set up the MinIO Client alias**  
   You must configure the `mc` client with an admin account to interact with your MinIO server. Use the following command to set up the alias:

   ```bash
   mc alias set minio https://s3.example.com minioadmin minioadmin
   ```

   Replace `https://s3.example.com` with your MinIO server endpoint, and `minioadmin` with your admin username and password.

4. **Access to a MinIO server**  
   Ensure you have access to a running MinIO server.

---

## Quick Start 🚀

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/netspeedy/python-s3cure.git
   cd python-s3cure
   ```

2. **Set Permissions**:
   ```bash
   chmod +x s3cure.py
   ```

3. **Run the Script**:
   ```bash
   ./s3cure.py --bucket-name <bucket_name> [--endpoint <s3_endpoint>]
   ```

---

## Example Usage 🔍

### 1. **Creating a New Bucket**
```bash
❯ ./s3cure.py -b testbucket

🌟 MinIO Bucket Creator - Resource Details 🌟
============================================================

🔑 Admin Credentials:
   • Username: testbucket
   • Password: NRTKcgPGS2a9hLAiefh3g8JV

🔐 Service Account Credentials:
   • Access Key: EFQQACIZ89I9HG5W9GX2
   • Secret Key: PQXH4V6wrlvjqcpEDDmbneoxdDsCBczGRab9fjtx
   • Bucket: testbucket
   • Endpoint: https://s3.example.com

============================================================
```

### 2. **When the Bucket Already Exists**
```bash
❯ ./s3cure.py -b testbucket

⚠️  Bucket 'testbucket' already exists.
```

---

## Security Features 🛡️

- 🔐 **Random Credential Generation**: Uses cryptographically secure methods to generate passwords and keys.
- 🔒 **Principle of Least Privilege**: Ensures that accounts and policies are scoped to the minimum required permissions.
- 🛡️ **Isolated Accounts**: Creates separate admin and service accounts for each bucket.

---

## Troubleshooting 🔧

### Common Issues and Solutions:

1. **Bucket Creation Fails**:
   - Ensure the MinIO client (`mc`) is installed and configured correctly.
   - Verify that the bucket name is valid and does not already exist.

2. **Service Account Issues**:
   - Check the MinIO server logs for errors.
   - Ensure the admin policy is correctly attached to the admin user.

3. **Policy Creation Fails**:
   - Verify that the MinIO client has the necessary permissions to create policies.

---

## Contributing 🤝

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a pull request.

---

## Support 💬

- 🎫 Issue Tracker: [GitHub Issues](https://github.com/netspeedy/python-s3cure/issues)

---

## Version History 📌

### 1.0.0 (2025-01-19)
- 🚀 Initial release
- 🪣 MinIO bucket creation
- 🔑 Admin and service account generation
- 🔒 Policy creation and attachment

---

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ by the Netspeedy Team*

*Last updated: January 19, 2025*
