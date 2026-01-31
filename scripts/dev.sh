#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${VENV_PATH:-${ROOT_DIR}/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP_MODULE="${APP_MODULE:-app:app}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
USE_DOCKER_DB="${USE_DOCKER_DB:-true}"

cd "${ROOT_DIR}"

create_venv() {
  if [[ -d "${VENV_PATH}" ]]; then
    return
  fi

  echo "Creando entorno virtual en ${VENV_PATH}..."
  "${PYTHON_BIN}" -m venv "${VENV_PATH}"
  "${VENV_PATH}/bin/pip" install --upgrade pip
  "${VENV_PATH}/bin/pip" install -r requirements.txt
}

maybe_start_db() {
  if [[ "${USE_DOCKER_DB}" != "true" ]]; then
    echo "Omitiendo docker-compose (USE_DOCKER_DB=${USE_DOCKER_DB})."
    return
  fi

  if ! command -v docker &>/dev/null; then
    echo "Docker no está instalado o en PATH; saltando base de datos en contenedor."
    return
  fi

  local compose_cmd="docker compose"
  if ! docker compose version &>/dev/null; then
    compose_cmd="docker-compose"
  fi

  echo "Levantando Postgres con docker-compose..."
  ${compose_cmd} up -d db
}

run_server() {
  echo "Iniciando FastAPI en http://${HOST}:${PORT}..."
  exec "${VENV_PATH}/bin/uvicorn" "${APP_MODULE}" --reload --host "${HOST}" --port "${PORT}"
}

create_venv
maybe_start_db
run_server
