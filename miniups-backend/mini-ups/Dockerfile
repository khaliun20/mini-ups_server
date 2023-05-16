FROM python:3.8-alpine

# Copy the rest of the code into the container
WORKDIR /app

# RUN pip3 install protobuf==3.20.0
ADD ./ /app/

# # Install any required dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /app/run_ups.sh

# Start the application
CMD ["/app/run_ups.sh" ]
