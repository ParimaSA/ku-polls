FROM python:3-alpine
# An argument needed to be passed

WORKDIR /app/polls

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
# Run application
CMD [ "./entrypoint.sh" ]