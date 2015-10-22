ps -e| grep uwsgi | awk '{print $1}' | xargs kill
