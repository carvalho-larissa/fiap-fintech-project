#!/usr/bin/env bash
# Espera o Oracle do container ficar pronto (máx. ~10 min) e mostra o status.
for i in $(seq 1 60); do
  if docker logs oracle-fintech 2>&1 | grep -q "DATABASE IS READY TO USE"; then
    echo "READY (checagem $i)"
    break
  fi
  if ! docker ps --format '{{.Names}}' | grep -q '^oracle-fintech$'; then
    echo "CONTAINER PARADO"; docker logs --tail 30 oracle-fintech 2>&1; exit 1
  fi
  sleep 10
done
docker ps -a --format '{{.Names}} | {{.Status}}'
docker logs oracle-fintech 2>&1 | grep -E "READY|ERROR|ORA-" | tail -5
