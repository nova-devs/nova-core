ARG image=dependencies

FROM $image

COPY . .

RUN mkdir -p assets/static \
  && python manage.py collectstatic --noinput