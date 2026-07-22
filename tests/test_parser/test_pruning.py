import openapi_python_client.schema as oai
from openapi_python_client.parser._pruning import get_reachable_classes
from openapi_python_client.parser.bodies import Body, BodyType
from openapi_python_client.parser.openapi import Endpoint
from openapi_python_client.parser.properties import Class
from openapi_python_client.parser.responses import NONE_SOURCE, HTTPStatusPattern, Response, Responses
from openapi_python_client.utils import ClassName, PythonIdentifier


def _class(name: str) -> Class:
    return Class(name=ClassName(name, ""), module_name=PythonIdentifier(name, ""))


def _endpoint(**kwargs) -> Endpoint:
    return Endpoint(
        path="/x",
        method="get",
        description=None,
        name="x",
        requires_security=False,
        tags=[],
        **kwargs,
    )


def _response(prop) -> Response:
    return Response(
        status_code=HTTPStatusPattern(pattern="200", code_range=(200, 200)),
        prop=prop,
        source=NONE_SOURCE,
        data=oai.Response.model_construct(description="ok"),
    )


class TestGetReachableClasses:
    def test_no_endpoints_reaches_nothing(self):
        assert get_reachable_classes(endpoints=[], classes_by_name={}) == set()

    def test_ignores_scalar_properties(self, string_property_factory):
        result = get_reachable_classes(
            endpoints=[_endpoint(query_parameters=[string_property_factory()])],
            classes_by_name={},
        )
        assert result == set()

    def test_collects_model_from_parameter(self, model_property_factory):
        thing = model_property_factory(class_info=_class("Thing"), required_properties=[], optional_properties=[])
        classes = {ClassName("Thing", ""): thing}
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[thing])], classes_by_name=classes)
        assert result == {"Thing"}

    def test_collects_required_optional_and_additional_properties(self, model_property_factory, enum_property_factory):
        status = enum_property_factory(name="status", class_info=_class("Status"))
        shared = model_property_factory(class_info=_class("Shared"), required_properties=[], optional_properties=[])
        extra = model_property_factory(class_info=_class("Extra"), required_properties=[], optional_properties=[])
        thing = model_property_factory(
            class_info=_class("Thing"),
            required_properties=[status],
            optional_properties=[shared],
            additional_properties=extra,
        )
        classes = {
            ClassName(name, ""): prop
            for name, prop in (("Thing", thing), ("Status", status), ("Shared", shared), ("Extra", extra))
        }
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[thing])], classes_by_name=classes)
        assert result == {"Thing", "Status", "Shared", "Extra"}

    def test_descends_through_list_inner_property(self, model_property_factory, list_property_factory):
        item = model_property_factory(class_info=_class("Item"), required_properties=[], optional_properties=[])
        listed = list_property_factory(inner_property=item)
        classes = {ClassName("Item", ""): item}
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[listed])], classes_by_name=classes)
        assert result == {"Item"}

    def test_descends_through_union_inner_properties(
        self, model_property_factory, literal_enum_property_factory, union_property_factory
    ):
        member = model_property_factory(class_info=_class("Member"), required_properties=[], optional_properties=[])
        kind = literal_enum_property_factory(name="kind", class_info=_class("Kind"))
        union = union_property_factory(inner_properties=[member, kind])
        classes = {ClassName("Member", ""): member, ClassName("Kind", ""): kind}
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[union])], classes_by_name=classes)
        assert result == {"Member", "Kind"}

    def test_descends_into_canonical_definition_not_stale_copy(self, model_property_factory, enum_property_factory):
        currency = enum_property_factory(name="currency", class_info=_class("Currency"))
        canonical_detail = model_property_factory(
            class_info=_class("Detail"), required_properties=[currency], optional_properties=[]
        )
        stale_detail = model_property_factory(
            class_info=_class("Detail"), required_properties=None, optional_properties=None
        )
        thing = model_property_factory(
            class_info=_class("Thing"), required_properties=[stale_detail], optional_properties=[]
        )
        classes = {
            ClassName("Thing", ""): thing,
            ClassName("Detail", ""): canonical_detail,
            ClassName("Currency", ""): currency,
        }
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[thing])], classes_by_name=classes)
        assert result == {"Thing", "Detail", "Currency"}

    def test_handles_self_referential_model(self, model_property_factory):
        node = model_property_factory(class_info=_class("Node"), required_properties=[], optional_properties=[])
        object.__setattr__(node, "optional_properties", [node])
        classes = {ClassName("Node", ""): node}
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[node])], classes_by_name=classes)
        assert result == {"Node"}

    def test_handles_mutual_cycle(self, model_property_factory):
        a = model_property_factory(class_info=_class("A"), required_properties=[], optional_properties=[])
        b = model_property_factory(class_info=_class("B"), required_properties=[], optional_properties=[])
        object.__setattr__(a, "optional_properties", [b])
        object.__setattr__(b, "optional_properties", [a])
        classes = {ClassName("A", ""): a, ClassName("B", ""): b}
        result = get_reachable_classes(endpoints=[_endpoint(query_parameters=[a])], classes_by_name=classes)
        assert result == {"A", "B"}

    def test_seeds_from_responses(self, model_property_factory):
        thing = model_property_factory(class_info=_class("RespModel"), required_properties=[], optional_properties=[])
        classes = {ClassName("RespModel", ""): thing}
        endpoint = _endpoint(responses=Responses(patterns=[_response(thing)], default=None))
        result = get_reachable_classes(endpoints=[endpoint], classes_by_name=classes)
        assert result == {"RespModel"}

    def test_seeds_from_default_response(self, model_property_factory):
        thing = model_property_factory(
            class_info=_class("DefaultModel"), required_properties=[], optional_properties=[]
        )
        classes = {ClassName("DefaultModel", ""): thing}
        endpoint = _endpoint(responses=Responses(patterns=[], default=_response(thing)))
        result = get_reachable_classes(endpoints=[endpoint], classes_by_name=classes)
        assert result == {"DefaultModel"}

    def test_seeds_from_bodies(self, model_property_factory):
        thing = model_property_factory(class_info=_class("BodyModel"), required_properties=[], optional_properties=[])
        classes = {ClassName("BodyModel", ""): thing}
        endpoint = _endpoint(bodies=[Body(content_type="application/json", prop=thing, body_type=BodyType.JSON)])
        result = get_reachable_classes(endpoints=[endpoint], classes_by_name=classes)
        assert result == {"BodyModel"}
