import re

from end_to_end_tests.functional_tests.helpers import (
    inline_spec_should_fail,
    with_generated_client_fixture,
)

MULTI_TAG_SPEC = """
paths:
  "/billing":
    post:
      operationId: createInvoice
      tags: ["billing"]
      requestBody:
        content:
          application/json:
            schema: {"$ref": "#/components/schemas/BillingModel"}
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/SharedModel"}
  "/users/me":
    get:
      operationId: getCurrentUser
      tags: ["users"]
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/SharedModel"}
  "/admin/settings":
    get:
      operationId: getAdminSettings
      tags: ["admin"]
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema: {"$ref": "#/components/schemas/AdminModel"}
  "/health":
    get:
      operationId: getHealth
      responses:
        "200":
          description: OK
components:
  schemas:
    SharedModel:
      type: object
      properties:
        id: {type: string}
        status: {"$ref": "#/components/schemas/OrderStatus"}
        address: {"$ref": "#/components/schemas/Address"}
    Address:
      type: object
      properties:
        city: {type: string}
    BillingModel:
      type: object
      properties:
        amount: {type: number}
    AdminModel:
      type: object
      properties:
        secret: {type: string}
    OrderStatus:
      type: string
      enum: ["active", "inactive"]
"""


def _generated_package(generated_client):
    return generated_client.output_path / generated_client.base_module


def _api_tag_dirs(generated_client) -> set[str]:
    api_dir = _generated_package(generated_client) / "api"
    return {child.name for child in api_dir.iterdir() if child.is_dir() and child.name != "__pycache__"}


def _model_modules(generated_client) -> set[str]:
    models_dir = _generated_package(generated_client) / "models"
    return {path.stem for path in models_dir.glob("*.py") if path.stem != "__init__"}


def _dangling_model_imports(generated_client) -> list[str]:
    package = _generated_package(generated_client)
    existing = {path.stem for path in (package / "models").glob("*.py")}
    dangling: list[str] = []
    for path in package.rglob("*.py"):
        for match in re.finditer(r"from \.+models\.(\w+) import", path.read_text()):
            if match.group(1) not in existing:
                dangling.append(f"{path.relative_to(package)} -> models.{match.group(1)}")
    return sorted(dangling)


@with_generated_client_fixture(MULTI_TAG_SPEC, extra_args=["--include-tags", "billing"])
class TestIncludeTagsViaCli:
    def test_only_included_tag_api_module_is_generated(self, generated_client):
        assert _api_tag_dirs(generated_client) == {"billing"}

    def test_unused_models_are_pruned(self, generated_client):
        assert _model_modules(generated_client) == {"billing_model", "shared_model", "order_status", "address"}

    def test_pruned_client_has_no_dangling_imports(self, generated_client):
        generated_client.import_module(".models")
        assert _dangling_model_imports(generated_client) == []


@with_generated_client_fixture(MULTI_TAG_SPEC, config="include_tags: [billing]")
class TestIncludeTagsViaConfigFile:
    def test_only_included_tag_api_module_is_generated(self, generated_client):
        assert _api_tag_dirs(generated_client) == {"billing"}

    def test_unused_models_are_pruned(self, generated_client):
        assert _model_modules(generated_client) == {"billing_model", "shared_model", "order_status", "address"}


@with_generated_client_fixture(MULTI_TAG_SPEC, extra_args=["--exclude-tags", "admin"])
class TestExcludeTagsViaCli:
    def test_excluded_tag_api_module_is_dropped(self, generated_client):
        assert _api_tag_dirs(generated_client) == {"billing", "users", "default"}

    def test_only_admin_models_are_pruned(self, generated_client):
        assert _model_modules(generated_client) == {"billing_model", "shared_model", "order_status", "address"}


@with_generated_client_fixture(MULTI_TAG_SPEC, config="exclude_tags: [admin]")
class TestExcludeTagsViaConfigFile:
    def test_excluded_tag_api_module_is_dropped(self, generated_client):
        assert _api_tag_dirs(generated_client) == {"billing", "users", "default"}

    def test_only_admin_models_are_pruned(self, generated_client):
        assert _model_modules(generated_client) == {"billing_model", "shared_model", "order_status", "address"}


class TestMutuallyExclusiveTagFlags:
    def test_both_flags_exits_nonzero(self):
        result = inline_spec_should_fail(
            MULTI_TAG_SPEC,
            extra_args=["--include-tags", "billing", "--exclude-tags", "admin"],
        )
        assert "Provide either include_tags or exclude_tags, not both" in result.output
