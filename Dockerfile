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

FROM ghcr.io/howaboutudance/hematite/python-base:3.10 as source
WORKDIR /app
COPY ./pyproject.toml ./ README.md ./ ./poetry.lock ./
RUN pip3 install poetry && poetry update --no-dev
COPY ./src/sample_module/. ./src/sample_module

FROM source as test
COPY ./src/test ./src/test ./src/conftest.py ./src/
RUN poetry update
CMD poetry run tox -e py38 && poetry run mypy sample_module/

FROM source as builder
RUN set +x && poetry build -f wheel && ls /app/dist

FROM ghcr.io/howaboutudance/hematite/python-slim:3.10 as app
COPY --from=builder /app/dist/. /app/dist/
WORKDIR /app
RUN set +x && pip3 install dist/sample_module*
CMD python -m sample_module