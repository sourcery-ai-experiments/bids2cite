import pytest
from utils import get_test_dir

from bids2cite.authors import get_author_info_from_orcid, parse_author
from bids2cite.bids2cite import main, update_bidsignore
from bids2cite.references import get_reference_id
from bids2cite.utils import print_unordered_list, prompt_format


def test_get_author_info_from_orcid():
    assert get_author_info_from_orcid("0000-0002-9120-8098") == {
        "affiliation": None,
        "firstname": "Melanie",
        "id": "ORCID:0000-0002-9120-8098",
        "lastname": "Ganz",
    }


def test_get_author_info_from_orcid_empty():
    assert get_author_info_from_orcid("8098") == {}


def test_parse_author_orcid():
    assert parse_author("0000-0002-9120-8098") == {
        "affiliation": None,
        "firstname": "Melanie",
        "id": "ORCID:0000-0002-9120-8098",
        "lastname": "Ganz",
    }


@pytest.mark.parametrize(
    "author,firstname,lastname",
    [
        ("  Bob  van der Bob  ", "Bob", "van der Bob"),
        ("   Bob,  van der  Bob  ", "Bob", "van der Bob"),
        ("Bob", "Bob", ""),
        ("Bob  ", "Bob", ""),
    ],
)
def test_parse_author(author, firstname, lastname):
    assert parse_author(author) == {"firstname": firstname, "lastname": lastname}


def test_prompt_format():

    assert prompt_format("foo") == "[bold]foo[/bold]"


def test_print_unordered_list():

    print_unordered_list(msg="bar", items=["foo"])


@pytest.mark.parametrize(
    "reference,expected",
    [
        ("pmid:1245  ", "pmid:1245"),
        ("  doi:1245", "doi:1245"),
        ("ncbi.nlm.nih.gov/pubmed/568", "pmid:568"),
        ("https://doi.org/10.666 ", "doi:10.666"),
    ],
)
def test_get_reference_id(reference, expected):
    assert get_reference_id(reference) == expected


def test_update_bidsignore():

    bids_dir = get_test_dir().joinpath("bids")
    update_bidsignore(bids_dir=bids_dir)

    bidsignore = bids_dir.joinpath(".bidsignore")
    with bidsignore.open("w") as f:
        f.write("foo")
    update_bidsignore(bids_dir=bids_dir)

    bids_dir.joinpath(".bidsignore").unlink(missing_ok=True)


def test_main():

    bids_dir = get_test_dir().joinpath("bids")
    main(
        bids_dir=bids_dir,
        description="add something",
        keywords=["foo", "bar"],
        skip_prompt=True,
    )

    bids_dir.joinpath(".bidsignore").unlink(missing_ok=True)
    bids_dir.joinpath("LICENSE").unlink(missing_ok=True)
    bids_dir.joinpath("datacite.yml").unlink(missing_ok=True)
