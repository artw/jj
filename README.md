# jj: Jinja Junkie

A FastAPI service that renders Jinja2 templates. Users specify the template and provide the necessary variables as query parameters.

## Usage

Store your templates under `./templates/`. Request a template using a tool like `curl` passing variable values as parameters. For example, for a template with the name `hello.j2` and content:

```
Hello {{ name }}!
```

You can fetch the rendered content with:

```bash
curl "http://localhost:8080/hello?name=World"
```
to get "Hello World!"

Errors will be returned if required variables are missing or if the template doesn't exist.
