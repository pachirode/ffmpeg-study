PROJ_ROOT_DIR=$(dirname "${BASH_SOURCE[0]}")/../..

REDIS_HOST=${REDIS_HOST:-0.0.0.0}
REDIS_PORT=${REDIS_PORT:-6379}
REDIS_PASSWORD=${REDIS_PASSWORD:-123456}

redis::pre_install(){
  util::sudo "apt install -y redis-tools"
}

redis::docker_install() {
  redis::pre_install

  docker run -d --name ffmpeg-study-redis \
    --restart always \
    --network ffmpeg-study \
    -v /data/ffpmeg-study/redis:/data \
    -p ${REDIS_HOST}:${REDIS_PORT}:6379 \
    redis:7.2.3 \
    redis-server \
    --appendonly yes \
    --save 60 1 \
    --protected-mode no \
    --requirepass ${REDIS_PASSWORD} \
    --loglevel debug

  sleep 2
  redis::status || return 1
  redis::info
}

redis::docker_uninstall() {
  docker rm -f ffpmge-study-redis &>/dev/null
  util::sudo "rm -rf /data/ffpmge-study/redis"
}

redis::install() {
  redis::pre_install

  util::sudo "mkdir -p /var/lib/redis"
  util::sudo "apt install -y -o Dpkg::Options::="--force-confmiss" --reinstall redis-server"

  # 修改配置
  redis_conf=/etc/redis/redis.conf
  [[ -f /etc/redis.conf ]] && redis_conf=/etc/redis.conf

  echo ${LINUX_PASSWORD} | sudo -S sed -i '/^daemonize/{s/no/yes/}' ${redis_conf}
  echo ${LINUX_PASSWORD} | sudo -S sed -i "s/^port.*/port ${REDIS_PORT}/g" ${redis_conf}
  echo ${LINUX_PASSWORD} | sudo -S sed -i '/^bind .*127.0.0.1/s/^/# /' ${redis_conf}
  echo ${LINUX_PASSWORD} | sudo -S sed -i 's/^# requirepass.*$/requirepass '"${REDIS_PASSWORD}"'/' ${redis_conf}
  echo ${LINUX_PASSWORD} | sudo -S sed -i '/^protected-mode/{s/yes/no/}' ${redis_conf}
  util::sudo "systemctl restart redis-server"
  redis::status || return 1
  redis::info
}

redis::uninstall() {
  redis_pid=$(pgrep -f redis-server)
  [[ ${redis_pid} != "" ]] && util::sudo "kill -9 ${redis_pid}"

  set +o errexit
  util::sudo "systemctl stop redis-server"
  util::sudo "systemctl disable redis-server"
  util::sudo "apt remove -y redis-server"
  util::sudo "rm -rf /var/lib/redis"
  set -o errexit
}

redis::info() {
  echo -e redis has been installed, here are some useful information:
  cat << EOF | sed 's/^/  /'
Redis access endpoint is: ${REDIS_HOST}:${REDIS_PORT}
       Redis password is: ${REDIS_PASSWORD}
     Redis Login Command: redis-cli --no-auth-warning -h ${REDIS_HOST} -p ${REDIS_PORT} -a '${REDIS_PASSWORD}'
EOF
}

redis::status()
{
  util::telnet ${REDIS_HOST} ${REDIS_PORT} || return 1
  redis-cli --no-auth-warning -h ${REDIS_HOST} -p ${REDIS_PORT} -a "${REDIS_PASSWORD}" --hotkeys || {
    onex::log::error "can not login with ${ONEX_REDIS_USERNAME}, redis maybe not initialized properly."
    return 1
  }
}

if [[ "$*" =~ redis:: ]]; then
  eval $*
fi
