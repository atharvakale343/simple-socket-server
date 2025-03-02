#!/system/bin/sh
HOST="35.82.27.154"
PORT=9999
BASE_MESSAGE="Hello from Gaia!"

conn_id=0

while true; do
    ((conn_id++))
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Attempting connection #$conn_id to $HOST:$PORT"
    
    # The inner loop sends a timestamped request with the connection ID every second.
    # nc -w 4 waits up to 4 seconds to establish a connection.
    ( while true; do 
         echo "[$(date +"%Y-%m-%d %H:%M:%S")] Request: $BASE_MESSAGE Client ConnID #$conn_id"
         sleep 1
      done ) | nc -w 4 "$HOST" "$PORT" | while IFS= read -r line; do
          echo "[$(date +"%Y-%m-%d %H:%M:%S")] Response: $line"
      done

    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Connection #$conn_id dropped or failed. Retrying in 1 second..."
    sleep 1
done
