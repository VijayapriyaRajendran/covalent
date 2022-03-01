from typing import Any, Optional, Sequence

from app import crud
from app.api import deps
from app.schemas.recipe import Recipe, RecipeCreate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", status_code=200, response_model=Sequence[Recipe])
def fetch_recipes(
    *,
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch all recipes
    """
    results = crud.recipe.get_all(db=db, limit=max_results)
    return results


@router.get("/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")

    return result


@router.delete("/{recipe_id}", status_code=200, response_model=Recipe)
def delete_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single recipe by ID
    """
    result = crud.recipe.remove(db=db, id=recipe_id)
    return result


@router.put("/{recipe_id}", status_code=201, response_model=Recipe)
def update_recipe(
    *, recipe_id: int, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Update a recipe in the database.
    """
    recipe = crud.recipe.get(db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=400, detail=f"Recipe with ID: {recipe_in.id} not found.")
    updated_recipe = crud.recipe.update(db=db, obj_in=recipe_in, db_obj=recipe)
    return updated_recipe


@router.post("/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)) -> dict:
    """
    Create a new recipe in the database.
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe
