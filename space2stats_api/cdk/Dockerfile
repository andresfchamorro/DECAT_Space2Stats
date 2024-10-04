FROM public.ecr.aws/lambda/python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN yum install -y gcc libpq-dev

COPY ./src/ ${LAMBDA_TASK_ROOT}/

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="$HOME/.local/bin:$PATH"

RUN $HOME/.local/bin/poetry config virtualenvs.create false \
    && $HOME/.local/bin/poetry install --no-dev --no-root

CMD ["space2stats.api.handler.handler"]