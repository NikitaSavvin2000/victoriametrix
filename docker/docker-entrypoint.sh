#!/bin/bash

# Проверка на инициализацию (не нужна для VictoriaMetrics, поэтому удалим)
# if [ ! -f /var/lib/grafana/.initialized ]; then
#   echo "Initializing Grafana..."
#   touch /var/lib/grafana/.initialized
# fi

echo "Starting VictoriaMetrics..."
exec /victoria-metrics-prod -retentionPeriod=100y
