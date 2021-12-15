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
ENV GS_CREDENTIALS '{"type": "service_account","project_id": "faceshot-backend-app","private_key_id": "3d7c251f827816090b844b6c4438b962a182e958","client_email": "cloudstorage@faceshot-backend-app.iam.gserviceaccount.com","token_uri": "https://oauth2.googleapis.com/token","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCzeQehtCKnTaA7\nZ92l1Isth4lahtmOBg+gOsDcXzq7zg6is5+eswxIPzN6oQlQPaLOOHJBGdJpGFwE\nKZihNl+RzGWCa3vGq+Ib0peCAcy5pX3Q8aTjghARs0xO7dcQ+S2M497w7i2+vq1O\ni3Wr6axzp99v7ASXOdB1VZ2QkQuDxGOMpnDT1SjkW86/r1/diKgJU2ikX6FGWwKg\nVBZ1vPkeNaCA5DkcYBQr0K/ACjHWTp5kwS3cxQd0Y6Gd267rSoKHSWc3OCmTuzeR\nvoQv6MIULt1Sbg12z6OLET8W4YCZZduJv1ec78WoD7JkZE7/HoQP1ilyCCwmzjjY\n/XXEEfezAgMBAAECggEANkhPBJulN5EE+7LImVWV2ul5o8XRm2E97KqYlo6/Bvql\n9pP5nVhuSJPFEDwQwxJBYbo05HfY6iyR+DhUj74QXdrCgRXdVBO8ycmCRbIhp6zk\nRwQvaRh3n8LpO544REv5ePma/qgrcdveMzl/F8YPgNOvgvyRzuOPp02D4KveHbYQ\nybTJ7YHbAySRr895jL56nydaPl1kyGMwFfT1cAzZCspNgW0QtymwquCG8Q5EQCCI\n0T/YKeKCk4Vz6vFMeJahNYqKxE+MO28zOd2HKa69aYR8Ete3DvU0o3xAv4VcZAHa\n1GkehGccf2I6QaLlyjmq0zZaP+L/ILmbBIDyc/NRcQKBgQDheczezoRi4DzNVVPJ\nDBZR73+d5ZUyja0g3q3rwph0mzt598j1SiqXQxJun9mtGU4mJfiU8AN5Rpehd1CR\noXajsCTgT6JLU9flYaGYhcpW8RouSnx44FgfP0mywF+KQVVqUhbecESutX+UnlyF\ngVhglGNEzS9c6CpiSJKtAB1FzwKBgQDLxO00sY1P4hUt8PfXpfl8il5TT8C0pU6k\nFfHAu4iewmx+4JW/mFGlCp3XGXVJYEnJ3tfEX8svGUMBkOvHBJ15sDhi3GWjAkqA\nvtbUr6XN/BQ5W9eE87WXWXvP3DOlr3gqDXqCjpGBpPXqodPtlkSJWAvxMbT/CJgq\nllvDxMkM3QKBgQDea7FuRRiRFRTFlRuOou7Nqs0f7F7OPLYBS8kTXaXYuVzlh0nk\ntmHnTxG6sNMhD2po9WIPQeibVMi1TibbUgTfmh32bHfziOTbcQDgnXIpa7Ng4LeC\n4gPr5xmDTIOytZpVxF6s1ODb20zcRY+NXzfYJej68NF8+8T7qQ2PvSIjPwKBgQCy\nmNKTKb/CsVSA5MBF2apW1uwftzoe2viXZshydawkAiKX/f4iZL3CmxCG9EBRZLyn\n29JfwtpSWKDbIYsV71yayLJTK/tFKX/lYd7noWAAr52GPJIkbHrPwdV79POrl6UJ\nrrCe95he+he0Y8xdZCSEAJDPARMzqPO99/VMHBFfXQKBgQCh++lFAR5SgD4eBK5c\nzVDbSfXBlTN3RcWD5QEUuR0zt7CwVTWXtgZNDOAIk05/JRvxJ3AWlcxWXg+y/5oK\nMef8gxf+SkA5AfZs96EBTdAtQKZ3SfPpRJHI4yHw2esrRpNV95oZ3n/Z5t+D08Ht\n9CxpMCckNIj3FDUOCzimAevV5Q==\n-----END PRIVATE KEY-----\n"}'
ENV GS_MODELS_BUCKET_NAME seed42_faceshot_backend_models
ENV GS_IMAGES_BUCKET_NAME seed42-faceshot-output-images

# CMD exec gunicorn --bind :$APP_PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec gunicorn --bind 0.0.0.0:7000 --timeout=300 wsgi:app