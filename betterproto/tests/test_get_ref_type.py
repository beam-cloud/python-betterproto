import pytest

from ..compile.importing import get_ref_type


@pytest.mark.parametrize(
    ["google_type", "expected_name", "expected_import"],
    [
        (
            ".google.protobuf.Empty",
            "betterproto_lib_google_protobuf.Empty",
            "import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf",
        ),
        (
            ".google.protobuf.Struct",
            "betterproto_lib_google_protobuf.Struct",
            "import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf",
        ),
        (
            ".google.protobuf.ListValue",
            "betterproto_lib_google_protobuf.ListValue",
            "import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf",
        ),
        (
            ".google.protobuf.Value",
            "betterproto_lib_google_protobuf.Value",
            "import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf",
        ),
    ],
)
def test_import_google_wellknown_types_non_wrappers(
    google_type: str, expected_name: str, expected_import: str
):
    imports = set()
    name = get_ref_type(package="", imports=imports, type_name=google_type)

    assert name == expected_name
    assert imports.__contains__(expected_import)


@pytest.mark.parametrize(
    ["google_type", "expected_name"],
    [
        (".google.protobuf.DoubleValue", "Optional[float]"),
        (".google.protobuf.FloatValue", "Optional[float]"),
        (".google.protobuf.Int32Value", "Optional[int]"),
        (".google.protobuf.Int64Value", "Optional[int]"),
        (".google.protobuf.UInt32Value", "Optional[int]"),
        (".google.protobuf.UInt64Value", "Optional[int]"),
        (".google.protobuf.BoolValue", "Optional[bool]"),
        (".google.protobuf.StringValue", "Optional[str]"),
        (".google.protobuf.BytesValue", "Optional[bytes]"),
    ],
)
def test_importing_google_wrappers_unwraps_them(google_type: str, expected_name: str):
    imports = set()
    name = get_ref_type(package="", imports=imports, type_name=google_type)

    assert name == expected_name
    assert imports == set()


@pytest.mark.parametrize(
    ["google_type", "expected_name"],
    [
        (".google.protobuf.DoubleValue", "betterproto_lib_google_protobuf.DoubleValue"),
        (".google.protobuf.FloatValue", "betterproto_lib_google_protobuf.FloatValue"),
        (".google.protobuf.Int32Value", "betterproto_lib_google_protobuf.Int32Value"),
        (".google.protobuf.Int64Value", "betterproto_lib_google_protobuf.Int64Value"),
        (".google.protobuf.UInt32Value", "betterproto_lib_google_protobuf.UInt32Value"),
        (".google.protobuf.UInt64Value", "betterproto_lib_google_protobuf.UInt64Value"),
        (".google.protobuf.BoolValue", "betterproto_lib_google_protobuf.BoolValue"),
        (".google.protobuf.StringValue", "betterproto_lib_google_protobuf.StringValue"),
        (".google.protobuf.BytesValue", "betterproto_lib_google_protobuf.BytesValue"),
    ],
)
def test_importing_google_wrappers_without_unwrapping(
    google_type: str, expected_name: str
):
    name = get_ref_type(package="", imports=set(), type_name=google_type, unwrap=False)

    assert name == expected_name


def test_import_child_package_from_package():
    imports = set()
    name = get_ref_type(
        package="package", imports=imports, type_name="package.child.Message"
    )

    assert imports == {"from . import child"}
    assert name == "child.Message"


def test_import_child_package_from_root():
    imports = set()
    name = get_ref_type(package="", imports=imports, type_name="child.Message")

    assert imports == {"from . import child"}
    assert name == "child.Message"


def test_import_camel_cased():
    imports = set()
    name = get_ref_type(
        package="", imports=imports, type_name="child_package.example_message"
    )

    assert imports == {"from . import child_package"}
    assert name == "child_package.ExampleMessage"


def test_import_nested_child_from_root():
    imports = set()
    name = get_ref_type(package="", imports=imports, type_name="nested.child.Message")

    assert imports == {"from .nested import child as nested_child"}
    assert name == "nested_child.Message"


def test_import_deeply_nested_child_from_root():
    imports = set()
    name = get_ref_type(
        package="", imports=imports, type_name="deeply.nested.child.Message"
    )

    assert imports == {"from .deeply.nested import child as deeply_nested_child"}
    assert name == "deeply_nested_child.Message"


def test_import_parent_package_from_child():
    imports = set()
    name = get_ref_type(
        package="package.child", imports=imports, type_name="package.Message"
    )

    assert imports == {"from .. import Message"}
    assert name == "Message"


def test_import_parent_package_from_deeply_nested_child():
    imports = set()
    name = get_ref_type(
        package="package.deeply.nested.child",
        imports=imports,
        type_name="package.deeply.nested.Message",
    )

    assert imports == {"from .. import Message"}
    assert name == "Message"


def test_import_root_package_from_child():
    imports = set()
    name = get_ref_type(package="package.child", imports=imports, type_name="Message")

    assert imports == {"from ... import Message"}
    assert name == "Message"


def test_import_root_package_from_deeply_nested_child():
    imports = set()
    name = get_ref_type(
        package="package.deeply.nested.child", imports=imports, type_name="Message"
    )

    assert imports == {"from ..... import Message"}
    assert name == "Message"


def test_import_root_sibling():
    imports = set()
    name = get_ref_type(package="", imports=imports, type_name="Message")

    assert imports == set()
    assert name == "Message"
