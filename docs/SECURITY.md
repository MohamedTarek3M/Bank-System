# Security Best Practices

## Overview

This document outlines security considerations and best practices for deploying and maintaining the Bank Management System.

## Production Deployment

### Secret Key Management

⚠️ **CRITICAL**: The application generates a random secret key on each startup. For production:

1. **Generate a persistent secret key:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Store it securely:**
   - Use environment variables
   - Never commit to version control
   - Use a secrets management service (AWS Secrets Manager, Azure Key Vault, etc.)

3. **Update app.py:**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
   ```

### HTTPS/SSL

- **Always use HTTPS in production**
- Obtain SSL certificates (Let's Encrypt, commercial CA)
- Configure `SESSION_COOKIE_SECURE = True` when using HTTPS
- Update session configuration:
  ```python
  app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
  app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
  app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
  ```

### Database Security

#### SQLite Considerations

- SQLite is suitable for development and small deployments
- For production with multiple users, consider PostgreSQL or MySQL
- Secure database file permissions: `chmod 600 database/bank_db.db`
- Regular backups: `cp database/bank_db.db backups/bank_db_$(date +%Y%m%d).db`

#### Database Encryption

For sensitive data, consider:
- Full disk encryption
- SQLCipher for encrypted SQLite databases
- Application-level encryption for sensitive fields

### Password Policy

Current requirements:
- Minimum 6 characters (increase to 8-12 for production)
- No complexity requirements (consider adding)

**Recommended improvements:**
```python
MIN_PASSWORD_LENGTH = 12
# Require: uppercase, lowercase, numbers, special characters
```

### Rate Limiting

Add rate limiting to prevent brute force attacks:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # ... login logic
```

### Input Validation

The system implements:
- ✅ Server-side validation for all inputs
- ✅ Parameterized SQL queries (prevents SQL injection)
- ✅ Password hashing (Werkzeug)
- ✅ Amount validation (min/max limits)
- ✅ Email format validation
- ✅ Username format validation

### Session Management

Current configuration:
- Session timeout: 30 minutes
- HttpOnly cookies: Enabled
- SameSite: Lax

**For production:**
- Consider shorter timeouts for admin/employee sessions
- Implement "Remember Me" functionality carefully
- Add session invalidation on password change

### Logging and Monitoring

**Implement logging:**
```python
import logging
logging.basicConfig(
    filename='bank_system.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log security events
logging.info(f"Login attempt: {username} from {request.remote_addr}")
logging.warning(f"Failed login: {username}")
```

**Monitor for:**
- Failed login attempts
- Large transactions
- Account modifications
- Database errors

### Backup Strategy

**Automated backups:**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp database/bank_db.db backups/bank_db_$DATE.db
# Keep only last 30 days
find backups/ -name "bank_db_*.db" -mtime +30 -delete
```

**Schedule with cron:**
```
0 2 * * * /path/to/backup.sh
```

### Environment Variables

Create `.env` file (never commit):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/bank_db.db
FLASK_ENV=production
DEBUG=False
```

### Deployment Checklist

- [ ] Change default admin password
- [ ] Set secure secret key
- [ ] Enable HTTPS
- [ ] Configure production database
- [ ] Set DEBUG=False
- [ ] Implement rate limiting
- [ ] Set up logging
- [ ] Configure backups
- [ ] Review file permissions
- [ ] Set up monitoring
- [ ] Document recovery procedures

### Additional Security Measures

1. **Two-Factor Authentication (2FA)**
   - Consider implementing for admin accounts
   - Use libraries like `pyotp`

2. **CSRF Protection**
   - Consider Flask-WTF for forms
   - Implement CSRF tokens

3. **Content Security Policy**
   ```python
   @app.after_request
   def set_csp(response):
       response.headers['Content-Security-Policy'] = "default-src 'self'"
       return response
   ```

4. **Security Headers**
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       response.headers['X-XSS-Protection'] = '1; mode=block'
       return response
   ```

## Incident Response

### If Compromised

1. **Immediately:**
   - Take system offline
   - Change all passwords
   - Rotate secret key
   - Review logs

2. **Investigation:**
   - Identify breach vector
   - Assess data exposure
   - Document timeline

3. **Recovery:**
   - Restore from clean backup
   - Apply security patches
   - Notify affected users

## Compliance

Depending on your jurisdiction and use case, consider:
- GDPR (EU)
- PCI DSS (payment cards)
- SOC 2
- Local banking regulations

## Support

For security issues:
- Do not create public issues
- Contact system administrator directly
- Follow responsible disclosure practices

## Legal & License

**CRITICAL**: This software is Proprietary. All Rights Reserved.
- Unauthourized access, modification, or distribution is prohibited.
- Usage is strictly limited to educational purposes as outlined in the [LICENSE](LICENSE) file.

---

**Last Updated:** 2025-12-13
**Review Schedule:** Quarterly
