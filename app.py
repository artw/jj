from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, meta, TemplateError
import os

app = FastAPI()

# Read TEMPLATE_DIR from environment or default to "templates/"
TEMPLATE_DIR = os.getenv("TEMPLATE_DIR", "templates/")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def get_query_params(request: Request):
    return request.query_params._dict

def get_required_template_vars(template_name: str):
    """Extract the required variables from a Jinja2 template."""
    template_source = env.loader.get_source(env, f"{template_name}.j2")[0]
    parsed_content = env.parse(template_source)
    return meta.find_undeclared_variables(parsed_content)

@app.get("/{template_name}")
async def render_template(request: Request, template_name: str, params: dict = Depends(get_query_params)):
    template_file = f"{template_name}.j2"

    # Check if the template file exists
    if not os.path.exists(os.path.join(TEMPLATE_DIR, template_file)):
        raise HTTPException(status_code=404, detail="Template not found")

    # Check for required parameters
    required_vars = get_required_template_vars(template_name)
    missing_vars = [var for var in required_vars if var not in params]

    if missing_vars:
        raise HTTPException(status_code=400, detail=f"Missing required parameters: {', '.join(missing_vars)}")

    try:
        return templates.TemplateResponse(template_file, {"request": request, **params})
    except TemplateError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

