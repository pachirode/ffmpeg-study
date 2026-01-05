PROJ_ROOT_DIR=$(dirname "${BASH_SOURCE[0]}")/../..

INSTALL_DIR=${PROJ_ROOT_DIR}/scripts/installation

source ${INSTALL_DIR}/redis.sh

install::pre_install() {
  util::sudo "apt update"
  util::sudo "apt install -y software-properties-common dirmngr apt-transport-https"
}

storage::docker_install() {
  redis::docker_install
}

storage::docker_uninstall() {
  redis::docker_uninstall
}

storage::install() {
  redis::install
}

storage::uninstall() {
  redis::uninstall
}

if [[ "$*" =~ onex::install:: ]]; then
  eval $*
fi
