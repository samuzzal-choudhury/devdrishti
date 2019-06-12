"""Test the code to retrieve package version from online sources."""

from unittest.mock import patch
import pytest

from f8a_utils.versions import (
    get_versions_for_npm_package,
    get_versions_for_pypi_package,
    get_versions_for_maven_package,
    get_versions_for_ep,
    get_latest_versions_for_ep
)


def test_get_versions_for_npm_package():
    """Test basic behavior of the function get_versions_for_npm_package."""
    package_versions = get_versions_for_npm_package("array")
    assert package_versions is not None

    # good old version 0.4.0 should be reported
    assert "0.4.0" in package_versions

    package_versions = get_versions_for_npm_package(
        "it is hard to specify package that does not exist"
    )
    assert package_versions is not None

    # we expect empty list there
    assert not package_versions

    package_versions = get_versions_for_ep("npm", "uuid")
    assert package_versions is not None
    assert "3.3.2" in package_versions


def test_get_versions_for_npm_package_deprecated_package():
    """Test basic behavior of the function get_versions_for_npm_package."""
    package_versions = get_versions_for_npm_package("nsp")
    assert package_versions is not None


class _response_no_json:
    """Mock the HTTP response that does not contain any payload."""

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return None


class _response_json_value_error:
    """Mock the HTTP response that raise ValueError during JSON conversion."""

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        raise ValueError(self.text)


def mocked_requests_get_no_json(url):
    """Implement mocked function requests.get()."""
    assert url
    return _response_no_json(200, """no JSON here""")


def mocked_requests_get_value_error(url):
    """Implement mocked function requests.get()."""
    assert url
    return _response_json_value_error(200, """no JSON here""")


@patch("requests.get", side_effect=mocked_requests_get_no_json)
def test_get_javascript_versions_empty_server_response(_mocked_get):
    """Test the behavior of function get_versions_for_npm_package for empty server response."""
    package_versions = get_versions_for_npm_package("array")
    # empty list is expected
    assert package_versions is not None
    assert not package_versions


@patch("requests.get", side_effect=mocked_requests_get_value_error)
def test_get_javascript_versions_server_response_without_json(_mocked_get):
    """Test get_versions_for_npm_package for server response w/o proper JSON."""
    package_versions = get_versions_for_npm_package("array")
    # empty list is expected
    assert package_versions is not None
    assert not package_versions


def test_get_python_versions():
    """Test basic behavior of function get_versions_for_pypi_package."""
    package_versions = get_versions_for_pypi_package("numpy")
    assert package_versions is not None

    # good old version 1.3.0 should be reported
    assert "1.3.0" in package_versions

    package_versions = get_versions_for_pypi_package(
        "it is hard to specify package that does not exist"
    )
    assert package_versions is not None

    # we expect empty list there
    assert not package_versions

    package_versions = get_versions_for_ep("pypi", "flask")
    assert package_versions is not None
    assert "1.0.2" in package_versions


def test_get_java_versions():
    """Test basic behavior of function get_versions_for_maven_package."""
    package_versions = get_versions_for_maven_package("tomcat:catalina")
    assert package_versions is not None

    # good old version 4.0.4 should be reported
    assert "4.0.4" in package_versions

    package_versions = get_versions_for_maven_package(
        "it is hard to specify package that does not exist:foobar"
    )
    assert package_versions is not None

    # we expect empty list there
    assert not package_versions

    package_versions = get_versions_for_maven_package("there's missing comma")
    assert package_versions is not None

    # we expect empty list there
    assert not package_versions

    package_versions = get_versions_for_ep("maven", "junit:junit")
    assert package_versions is not None
    assert "4.12" in package_versions


def test_get_versions_for_ep_bad_ecosystem():
    """Test get_versions_for_ep for unsupported ecosystem."""
    with pytest.raises(ValueError):
        get_versions_for_ep("cobol", "cds-parsers")


def test_get_versions_for_ep_no_package():
    """Test get_versions_for_ep for no package provided."""
    with pytest.raises(ValueError):
        get_versions_for_ep("maven", None)
    with pytest.raises(ValueError):
        get_versions_for_ep("npm", None)
    with pytest.raises(ValueError):
        get_versions_for_ep("pypi", None)


def test_get_versions_for_ep_no_ecosystem():
    """Test get_versions_for_ep for no ecosystem provided."""
    with pytest.raises(ValueError):
        get_versions_for_ep(None, "cds-parsers")


def test_get_latest_versions_for_ep():
    """Test basic behavior of function get_latest_versions_for_ep."""
    package_versions = get_latest_versions_for_ep("maven", "tomcat:catalina")
    assert package_versions is not None

    package_versions = get_latest_versions_for_ep("maven", "org.abcl:abcl")
    assert package_versions is not None

    package_versions = get_latest_versions_for_ep("pypi", "numpy")
    assert package_versions is not None

    package_versions = get_latest_versions_for_ep("npm", "array")
    assert package_versions is not None

    package_versions = get_latest_versions_for_ep("npm", "lerna-tt-pk2-sy")
    assert package_versions is not None

    package_versions = get_latest_versions_for_ep("npm", "abyzdeopkl")
    assert not package_versions

    package_versions = get_latest_versions_for_ep("maven", "abyzdeopkl")
    assert not package_versions

    package_versions = get_latest_versions_for_ep("pypi", "abyzdeopkl")
    assert not package_versions

    with pytest.raises(ValueError):
        get_latest_versions_for_ep("cobol", "cds-parsers")

    with pytest.raises(ValueError):
        get_latest_versions_for_ep("maven", None)
