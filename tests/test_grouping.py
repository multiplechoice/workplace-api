from app import group_results

examples = [
    {
        "company": "Landsvirkjun",
        "created_at": "2017-05-08T00:00:00+00:00",
        "id": "0bbbf945-36a7-4ae9-a995-f440ea1fde29",
        "last_modified": "2017-06-16T22:08:54.525875+00:00",
        "posted": "2017-08-05T00:00:00",
        "spider": "visir",
        "title": "Viu00f0 leitum au00f0 kraftmiklum einstaklingum u00ed spennandi stu00f6rf",
        "url": "https://job.visir.is/display-job/4650/Viu00f0-leitum-au00f0-kraftmiklum-einstaklingum-u00ed-spennandi-stu00f6rf.html"
    },
    {
        "company": "Gru00f3u00f0rarstu00f6u00f0in Lambhagi ehf",
        "created_at": "2017-05-08T00:00:00+00:00",
        "id": "5cecfb1d-07fd-4d44-938a-a13adf7987e1",
        "last_modified": "2017-06-16T22:08:54.525875+00:00",
        "posted": "2017-08-05T00:00:00",
        "spider": "visir",
        "title": "Starfmau00f0ur /  Stju00f3rna pu00f6kkun",
        "url": "https://job.visir.is/display-job/4699/Starfmau00f0ur----Stju00f3rna-pu00f6kkun.html"
    },
    {
        "company": None,
        "created_at": "2017-06-21T10:13:10.431965+00:00",
        "deadline": "2017-07-21",
        "id": "18c7d431-d315-45fb-b0c6-6aff5399f8d5",
        "last_modified": "2017-06-21T10:13:10.431965+00:00",
        "posted": "2017-06-21",
        "spider": "mbl",
        "title": "Ertu fram\u00farskarandi? T\u00e6knima\u00f0ur",
        "url": "http://www.mbl.is/atvinna/3708/"
    },
    {
        "company": "Ruby Tuesday",
        "created_at": "2017-06-21T10:25:32.927728+00:00",
        "deadline": "2017-05-07T00:00:00",
        "id": "1069831f-56c0-4f56-a9cc-6e72ed3ec456",
        "last_modified": "2017-06-21T10:25:32.927728+00:00",
        "posted": "2017-06-20T19:30:00",
        "spider": "alfred",
        "title": "\u00dej\u00f3nn \u00ed hlutastarf",
        "url": "https://alfred.is/starf/11396"
    },
    {
        "company": "Joe & the juice",
        "created_at": "2017-06-21T10:25:32.927728+00:00",
        "deadline": "2017-04-07T00:00:00",
        "id": "83cc07a1-8d44-4290-82ed-b0315c0e5d84",
        "last_modified": "2017-06-21T10:25:32.927728+00:00",
        "posted": "2017-06-20T16:20:00",
        "spider": "alfred",
        "title": "Viltu dj\u00fasa me\u00f0 okkur?",
        "url": "https://alfred.is/starf/11395"
    },
    {
        "company": "CPLA ehf",
        "created_at": "2017-06-21T10:25:32.927728+00:00",
        "deadline": "2017-06-27T00:00:00",
        "id": "1432bac9-e21e-457a-9bae-662937090eb0",
        "last_modified": "2017-06-21T10:25:32.927728+00:00",
        "posted": "2017-06-20T16:08:00",
        "spider": "alfred",
        "title": "Starfsma\u00f0ur \u00ed gestam\u00f3t\u00f6ku kv\u00f6ld og n\u00e6turvakt",
        "url": "https://alfred.is/starf/11394"
    },
    {
        "company": "Frakt",
        "created_at": "2017-06-21T10:25:32.927728+00:00",
        "deadline": "2017-06-25T00:00:00",
        "id": "4a8ae55e-89c3-4e38-b539-2a2cdb393319",
        "last_modified": "2017-06-21T10:25:32.927728+00:00",
        "posted": "2017-06-20T15:57:00",
        "spider": "alfred",
        "title": "Tollsk\u00fdrsluger\u00f0 - afleysingar",
        "url": "https://alfred.is/starf/11393"
    }
]


def test_group_by_spider():
    grouped = group_results(examples, 'spider')
    assert sorted(grouped.keys()) == ['alfred', 'mbl', 'visir']
    assert len(grouped['alfred']) == 4
    assert grouped['alfred'] == examples[3:]
    assert len(grouped['mbl']) == 1
    assert grouped['mbl'] == [examples[2]]
    assert len(grouped['visir']) == 2
    assert grouped['visir'] == examples[0:2]


def test_group_when_key_missing():
    grouped = group_results(examples, 'this_key_doesnt_exist')
    assert list(grouped.keys()) == ['unknown']
    assert grouped['unknown'] == examples


def test_partial_grouping_with_missing_key():
    simple_examples = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
        {'id': 3},
    ]
    assert group_results(simple_examples, 'name') == {
        'Alice': [{'id': 1, 'name': 'Alice'}],
        'Bob': [{'id': 2, 'name': 'Bob'}],
        'unknown': [{'id': 3}]
    }
