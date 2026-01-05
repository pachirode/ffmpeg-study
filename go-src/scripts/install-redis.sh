set -o errexit
set -o nounset
set -o pipefail

PROJ_ROOT_DIR=$(dirname "${BASH_SOURCE[0]}")/..
source "${PROJ_ROOT_DIR}/scripts/installation/install.sh"
source "${PROJ_ROOT_DIR}/scripts/installation/redis.sh"
source "${PROJ_ROOT_DIR}/scripts/lib/util.sh"
source "${PROJ_ROOT_DIR}/scripts/lib/common.sh"

common::network
redis::docker_install
