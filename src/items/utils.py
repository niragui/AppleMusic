

def get_relationship(relationships: dict,
                     relationship_name: str):
    """
    Extract the data inside a relationship.
    Returns None if not found

    Parameters:
        - relationships: Dictionary with all the relationships
        - relationship_name: Name of the relationship to extract
    """
    searched_relation = relationships.get(relationship_name, None)
    if searched_relation is None:
        return None

    if "data" in searched_relation:
        searched_relation = searched_relation["data"]

    return searched_relation
