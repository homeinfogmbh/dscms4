"""Common ORM related functions."""


__all__ = ['resolve_refs']


def resolve_refs(model_class, reference_instance, current_models, new_json, *,
                 identifier_model=lambda model: model.id,
                 identifier_json=lambda obj: obj.get('id')):
    """Resolves referenced models for JSON deserialization and patching."""

    current_models = frozenset(current_models)
    new_ids = {identifier_json(obj) for obj in new_json}
    unchanged_models = {
        model for model in current_models
        if identifier_model(model) in new_ids}
    delete_models = {
        model for model in current_models
        if identifier_model(model) not in new_ids}
    not_new_models = unchanged_models | delete_models
    not_new_ids = {identifier_model(model) for model in not_new_models}
    new_json = {
        obj for obj in new_json if identifier_json(obj) not in not_new_ids}
    new_models = {
        model_class.from_json(obj, reference_instance) for obj in new_json}
    return (new_models, delete_models)
