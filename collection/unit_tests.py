import pytest

from collection.finance import obv_map_function, true_range_map_function, get_ccis, get_obvs


@pytest.mark.parametrize("row, prev_obv, expected", [
    ({"close_p": 105, "open_p": 100, "volume_q": 1000}, 5000, 6000),
    ({"close_p": 95, "open_p": 100, "volume_q": 1000}, 5000, 4000),
    ({"close_p": 100, "open_p": 100, "volume_q": 1000}, 5000, 5000),
])
def test_obv_map_function(row, prev_obv, expected):
    assert obv_map_function(row, prev_obv) == expected


@pytest.mark.parametrize("row, prev_close, expected", [
    ({"high_p": 110, "low_p": 90}, 100, 20),
    ({"high_p": 120, "low_p": 80}, 100, 40),
    ({"high_p": 105, "low_p": 95}, 100, 10),
])
def test_true_range_map_function(row, prev_close, expected):
    assert true_range_map_function(row, prev_close) == expected


def test_get_ccis():
    input_list = [
        {
            "date_time": "24-Aug-10",
            "typical_price": 23.9826
        },
        {
            "date_time": "25-Aug-10",
            "typical_price": 23.9164
        },
        {
            "date_time": "26-Aug-10",
            "typical_price": 23.7872
        },
        {
            "date_time": "27-Aug-10",
            "typical_price": 23.6745
        },
        {
            "date_time": "30-Aug-10",
            "typical_price": 23.5420
        },
        {
            "date_time": "31-Aug-10",
            "typical_price": 23.3615
        },
        {
            "date_time": "1-Sep-10",
            "typical_price": 23.6513
        },
        {
            "date_time": "2-Sep-10",
            "typical_price": 23.7209
        },
        {
            "date_time": "3-Sep-10",
            "typical_price": 24.1649
        },
        {
            "date_time": "7-Sep-10",
            "typical_price": 23.9131
        },
        {
            "date_time": "8-Sep-10",
            "typical_price": 23.8104
        },
        {
            "date_time": "9-Sep-10",
            "typical_price": 23.9230
        },
        {
            "date_time": "10-Sep-10",
            "typical_price": 23.7441
        },
        {
            "date_time": "13-Sep-10",
            "typical_price": 24.6784
        },
        {
            "date_time": "14-Sep-10",
            "typical_price": 24.9368
        },
        {
            "date_time": "15-Sep-10",
            "typical_price": 24.9318
        },
        {
            "date_time": "16-Sep-10",
            "typical_price": 25.0958
        },
        {
            "date_time": "17-Sep-10",
            "typical_price": 25.1223
        },
        {
            "date_time": "20-Sep-10",
            "typical_price": 25.1985
        },
        {
            "date_time": "21-Sep-10",
            "typical_price": 25.0627
        },
        {
            "date_time": "22-Sep-10",
            "typical_price": 24.4961
        },
        {
            "date_time": "23-Sep-10",
            "typical_price": 24.3106
        },
        {
            "date_time": "24-Sep-10",
            "typical_price": 24.5674
        },
        {
            "date_time": "27-Sep-10",
            "typical_price": 24.6196
        },
        {
            "date_time": "28-Sep-10",
            "typical_price": 24.4920
        },
        {
            "date_time": "29-Sep-10",
            "typical_price": 24.3703
        },
        {
            "date_time": "30-Sep-10",
            "typical_price": 24.4100
        },
        {
            "date_time": "1-Oct-10",
            "typical_price": 24.3504
        },
        {
            "date_time": "4-Oct-10",
            "typical_price": 23.7474
        },
        {
            "date_time": "5-Oct-10",
            "typical_price": 24.0887
        }
    ]
    ccis = get_ccis(input_list)
    print(ccis)
    for cci in ccis:
        print(f"{cci["date_time"]}: {cci["CCI"]}")
    assert len(ccis) == 11
    assert round(ccis[0]["CCI"], 5) == 102.31841
    assert round(ccis[-1]["CCI"], 5) == -73.06346
