#FROM python:3.6.9-slim-stretch
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
RUN apt-get update && apt-get install -y pkg-config \
                                        build-essential \
                                        python3-pip \
                                        python3-dev \
                                        python3-distutils \
                                        python3-pkg-resources \
                                        python3-tk \
                                        git \
                                        libquadmath0
#                                         python3-opencv \
#                                         libgl1-mesa-glx \
#                                         ffmpeg \
#                                         libsm6 \
#                                         libxext6

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/logs && touch /app/logs/faceshot_backend_app.log
WORKDIR /app
RUN mkdir -p /app/tmp
RUN mkdir -p /app/models
COPY src/ .

ENV APP_HOST 0.0.0.0
ENV APP_PORT 7000
ENV APP_LOG_PATH /app/logs
ENV APP_LOG_LEVEL DEBUG
ENV APP_TEMP_PATH /app/tmp
ENV APP_PRETRAINED_MODELS_PATH /app/models
ENV GS_CREDENTIALS '{"type": "service_account", "project_id": "seed42-faceshot-phase2", "private_key_id": "964630fca9c141f6efb5c77c11f16526c2d6c3e6", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD79L8zcipSEl3z\nS9X5sapjtlRcI58yfFNAps3dC3uXrR6gWFnMHJ2k2DZB9NZNF/1brwoKldN84gcA\nTlDpxX6IerN3rivcQ5vg4gKy+LKcDBSEYhb05tFlyq1Apu8KD/cqTfBvsTl952Qu\n1Vp4n09Hs7lykaDVrxENmKSTRCT32+jui3r6B5cUlZalFJvXwX1+yL1mc1xJL9K/\nd8mUE1LOwN18vaCxZupGKa87SaH4I+oRRJhQZwxSeWzqJ0v35AuKmDyFd/0IoTNL\nA+Cg6B6P2Xnujh6ud8MIlcW/PpFxlAQV6RlTKkRwbXXIbJ9HJRVwSKDlg59dn98n\nKyLjkL2nAgMBAAECggEAAJi2lS1u2o05lLhivs8ZYK1kq2fYL3s/iovP4/dBfn1F\n8R+UbYPJ1G3rSaJbRDPLgUU7qFpsyu28EizyoG27xstHk9UhPHRv24tIHLAIYuSH\nwz0k4cU5d1y7UUez5tmyfkf7SusSqvDPz2k+PW00d65+FhPbMMupJizs2CkVT1Lq\n7o5SL+695oJ5osIS1qWC9SKa7bDJJOFVNE4DBT+OVjrVZ0k8r2RJJ5zHKjJTWd/R\n3HCDtzfDFTF12/viJZpIcOdlIZjss+pPYXwefeGJKS4xfgrzGSBgB9vbKiuMWLV2\nZgBKGP72xw/O165Ms5D3+d9Y06CrE+aXQ3/96pfmZQKBgQD/cY76LS91lpHVVREe\nWgNIR+OR6ZXKCMJARgtzBPV7r802JgsCOlOGd/yPOaDTjQCjC0DsoDR+cLE/WuDX\nU3V6ZXpEeamgT8pMk2YPTau2ljLiYLF0DgMeqMJbRpp84TNFb0l+KE2OeFbrvzf/\nRzu5ZHlpslTIfOwxe3tPELV/FQKBgQD8gT5e1cKu9qh/wlT/dx26DzIOrXUUULCG\nss+d5eHBefYu+lmTQPQ9wIniLfIlQVXCVWlt/GbaZfkJWuemKRWttXkzulJnb2Z/\nqmr8fulLkjn3riEtY3SoY0/wnWk1aV8xX+ucWK5WyTORwO2Z5YIsvOi8DcuCn0FL\nFJR3148YywKBgCFVSDsNOmw1wcH838b+J/9+ogugV5ONoQuSGFxiAUaqojS2sikQ\nQ2YAskxeUMZKWBLunQJDxZXaTsbdrQlsMqBOLa5R0fjBcLydX2wPzqB86RbxVza1\nvWJ60yHmDLLPEEm3Q/faeoRk37LTuRLu0LRYkB9izf17j7bFTkn6/DQhAoGBALt7\n52iZBW3N/XynOV9Z/XuKDtvxFS6ZXwkUua1+4+o5eX6WKm542yEC1h5XiST6Zwfd\nTWP59hCRiKDWm4u3k74gMbcj0E223H9MdRW30ddn4pyx8TZ3U0Y4P0HkTxr2e1T4\n6MN04TXVPPIrMwCC9e3r8k63W3VIdD2gMUDuj/STAoGBAJ0R3LbfUrb+h1j9c2bX\noEYhEn6nK8JThdBZXzz/dRREmaQvi3+s80w1XHiF2TRQw1hinMnPSg4KfcIG2G5B\nV40MJMHzVAGHcbj0LB6tTwXCBQV6MfrwwV3TtjQGYxxJbpOzRLsYLCkfij4BIdSw\n47DtUDH67J2xzl+sgb2PfrH4\n-----END PRIVATE KEY-----\n", "client_email": "faceshot-admin@seed42-faceshot-phase2.iam.gserviceaccount.com", "client_id": "118065560946495260723", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/faceshot-admin%40seed42-faceshot-phase2.iam.gserviceaccount.com"}'
ENV GS_MODELS_BUCKET_NAME seed42-faceshot-phase2-models
ENV GS_IMAGES_BUCKET_NAME seed42-faceshot-phase2-output-images

# CMD exec gunicorn --bind :$APP_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind 0.0.0.0:7000 --timeout=300 wsgi:app