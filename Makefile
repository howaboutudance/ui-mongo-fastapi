# Copyright 2021 Michael Penhallegon 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SAMPLE_TAG = hematite/pytemplate-docker
SAMPLE_INTERACT = hematite/pytemplate-interact
SAMPLE_TEST = hematite/pytemplate-test
DOCKER_BUILD=docker build ./ -f Dockerfile
DOCKER_RUN=docker run
VENV_VERSION_FOLDER := venv$(shell python3 --version | sed -ne 's/[^0-9]*\(\([0-9]*\.\)\{0,2\}\).*/\1/p' | sed -e "s/\.//g")

init-env: FORCE
	pyenv local 3.10.0 3.9.8 3.8.12 3.7.12
	pip3 install poetry
	poetry update
	poetry shell

build: FORCE
	${DOCKER_BUILD} --no-cache=true --target=app -t ${SAMPLE_TAG}

run:
	${DOCKER_RUN} ${SAMPLE_TAG}

interact: FORCE
	${DOCKER_BUILD} --target=interact -t ${SAMPLE_TEST}
	${DOCKER_RUN} -it ${SAMPLE_INTERACT}

test: FORCE
	${DOCKER_BUILD} --target=test -t ${SAMPLE_INTERACT}
	${DOCKER_RUN} -it ${SAMPLE_INTERACT}

local-test: FORCE
	tox
	mypy sample_module/

FORCE: