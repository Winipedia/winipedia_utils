"""Tests for winipedia_utils.data.dataframe.cleaning module."""

import random
from collections.abc import Callable
from typing import Any

import polars as pl
import pytest
from pytest_mock import MockerFixture

from winipedia_utils.data.dataframe.cleaning import CleaningDF
from winipedia_utils.testing.assertions import assert_with_msg


class MyCleaningDF(CleaningDF):
    """Concrete implementation of CleaningDF for testing."""

    STR_COL = "str_col"
    INT_COL = "int_col"
    FLOAT_COL = "float_col"
    FLOAT_COL_2 = "float_col_2"
    BOOL_COL = "bool_col"

    @classmethod
    def get_rename_map(cls) -> dict[str, str]:
        """Test implementation of rename_map."""
        return {
            cls.STR_COL: "str_col_old",
            cls.INT_COL: "int_col_old",
            cls.FLOAT_COL: "float_col_old",
            cls.FLOAT_COL_2: "float_col_2_old",
            cls.BOOL_COL: "bool_col_old",
        }

    @classmethod
    def get_col_dtype_map(cls) -> dict[str, type[pl.DataType]]:
        """Test implementation of col_cls_map."""
        return {
            cls.STR_COL: pl.Utf8,
            cls.INT_COL: pl.Int64,
            cls.FLOAT_COL: pl.Float64,
            cls.FLOAT_COL_2: pl.Float64,
            cls.BOOL_COL: pl.Boolean,
        }

    @classmethod
    def get_drop_null_subsets(cls) -> tuple[tuple[str, ...], ...]:
        """Test implementation of drop_null_subsets."""
        return ((cls.STR_COL, cls.INT_COL), (cls.FLOAT_COL, cls.BOOL_COL))

    @classmethod
    def get_fill_null_map(cls) -> dict[str, Any]:
        """Test implementation of fill_null_map."""
        return {
            cls.STR_COL: "",
            cls.INT_COL: 0,
            cls.FLOAT_COL: 0.0,
            cls.FLOAT_COL_2: 0.0,
            cls.BOOL_COL: False,
        }

    @classmethod
    def get_sort_cols(cls) -> tuple[tuple[str, bool], ...]:
        """Test implementation of sort_cols."""
        return ((cls.INT_COL, False), (cls.STR_COL, True))

    @classmethod
    def get_unique_subsets(cls) -> tuple[tuple[str, ...], ...]:
        """Test implementation of unique_subsets."""
        return ((cls.STR_COL, cls.INT_COL), (cls.FLOAT_COL, cls.BOOL_COL))

    @classmethod
    def get_no_null_cols(cls) -> tuple[str, ...]:
        """Test implementation of not_null_cols."""
        return (cls.STR_COL, cls.INT_COL)

    @classmethod
    def get_col_converter_map(
        cls,
    ) -> dict[str, Callable[[pl.Series], pl.Series]]:
        """Test implementation of col_converter_map."""
        # lets add 1 to the int_col
        return {
            cls.FLOAT_COL: cls.skip_col_converter,
            cls.FLOAT_COL_2: lambda x: x * 2,
            cls.INT_COL: lambda x: x + 1,
            cls.STR_COL: cls.skip_col_converter,
            cls.BOOL_COL: cls.skip_col_converter,
        }

    @classmethod
    def get_add_on_duplicate_cols(cls) -> tuple[str, ...]:
        """Test implementation of add_on_duplicate_cols."""
        return (cls.FLOAT_COL, cls.INT_COL)

    @classmethod
    def get_col_precision_map(cls) -> dict[str, int]:
        """Test implementation of col_precision_map."""
        return {cls.FLOAT_COL: 2, cls.FLOAT_COL_2: 2}


class TestCleaningDF:
    """Test class for CleaningDF."""

    def get_dirty_data(self) -> dict[str, list[Any]]:
        """Get dirty data for testing."""
        return {
            "str_col_old": ["a", "b", "c"],
            "int_col_old": [0, 1, 2],
            "float_col_old": [0.0, 1.1234, 2.5678],
            "float_col_2_old": [0.0, 1.1234, 2.5678],
            "bool_col_old": [True, False, True],
        }

    def get_cleaning_df(self) -> CleaningDF:
        """Get clean data for testing."""
        return MyCleaningDF(self.get_dirty_data())

    def test___init__(self) -> None:
        """Test method for __init__."""
        c_df = self.get_cleaning_df()
        expected = (
            len(self.get_dirty_data()[next(iter(self.get_dirty_data().keys()))]),
            len(self.get_dirty_data()),
        )
        assert_with_msg(
            c_df.df.shape == expected,
            f"Expected df shape {expected}, got {c_df.df.shape}",
        )

    def test_get_rename_map(self) -> None:
        """Test method for rename_map."""
        rename_map = MyCleaningDF.get_rename_map()
        assert_with_msg(
            all(isinstance(c, str) for c in rename_map),
            "Expected all keys and values to be strings",
        )

    def test_get_col_dtype_map(self) -> None:
        """Test method for col_cls_map."""
        col_cls_map = MyCleaningDF.get_col_dtype_map()
        # assert all types are polars types
        assert_with_msg(
            all(issubclass(t, pl.DataType) for t in col_cls_map.values()),
            "Expected all types to be polars types",
        )
        # assert all colnames are strings
        assert_with_msg(
            all(isinstance(c, str) for c in col_cls_map),
            "Expected all column names to be strings",
        )

    def test_get_drop_null_subsets(self) -> None:
        """Test method for drop_null_subsets."""
        # assert it returns a tuple of tuples with colnames that are in col_names
        drop_null_subsets = MyCleaningDF.get_drop_null_subsets()
        assert_with_msg(
            all(
                c in MyCleaningDF.get_col_dtype_map()
                for t in drop_null_subsets
                for c in t
            ),
            "Expected all elements in the tuples to be column names",
        )
        assert_with_msg(
            all(isinstance(t, tuple) for t in drop_null_subsets),
            "Expected drop_null_subsets to return a tuple of tuples",
        )

    def test_get_fill_null_map(self) -> None:
        """Test method for fill_null_map."""
        fill_null_map = MyCleaningDF.get_fill_null_map()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c in fill_null_map),
            "Expected all keys to be column names",
        )
        assert_with_msg(
            all(isinstance(v, (int, float, str, bool)) for v in fill_null_map.values()),
            "Expected all values to be int, float, str or bool",
        )

    def test_get_sort_cols(self) -> None:
        """Test method for sort_cols."""
        sort_cols = MyCleaningDF.get_sort_cols()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c, _ in sort_cols),
            "Expected all elements in the tuples to be column names",
        )

    def test_get_unique_subsets(self) -> None:
        """Test method for unique_subsets."""
        unique_subsets = MyCleaningDF.get_unique_subsets()
        assert_with_msg(
            all(
                c in MyCleaningDF.get_col_dtype_map() for t in unique_subsets for c in t
            ),
            "Expected all elements in the tuples to be column names",
        )

    def test_get_no_null_cols(self) -> None:
        """Test method for not_null_cols."""
        not_null_cols = MyCleaningDF.get_no_null_cols()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c in not_null_cols),
            "Expected all elements to be column names",
        )

    def test_get_col_converter_map(self) -> None:
        """Test method for col_converter_map."""
        col_converter_map = MyCleaningDF.get_col_converter_map()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c in col_converter_map),
            "Expected all keys to be column names",
        )

    def test_get_add_on_duplicate_cols(self) -> None:
        """Test method for add_on_duplicate_cols."""
        add_on_duplicate_cols = MyCleaningDF.get_add_on_duplicate_cols()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c in add_on_duplicate_cols),
            "Expected all elements to be column names",
        )

    def test_get_col_precision_map(self) -> None:
        """Test method for col_precision_map."""
        col_precision_map = MyCleaningDF.get_col_precision_map()
        assert_with_msg(
            all(c in MyCleaningDF.get_col_dtype_map() for c in col_precision_map),
            "Expected all keys to be column names",
        )
        assert_with_msg(
            all(isinstance(v, int) for v in col_precision_map.values()),
            "Expected all values to be integers",
        )

    def test_clean(self) -> None:
        """Test method for clean."""
        c_df = self.get_cleaning_df()
        expected = (
            len(self.get_dirty_data()[next(iter(self.get_dirty_data().keys()))]),
            len(self.get_dirty_data()),
        )
        assert_with_msg(
            c_df.df.shape == expected,
            f"Expected df shape {expected}, got {c_df.df.shape}",
        )

    def test_rename_cols(self) -> None:
        """Test method for rename_cols."""
        c_df = self.get_cleaning_df()
        assert_with_msg(
            all(c in c_df.df.columns for c in MyCleaningDF.get_col_dtype_map()),
            "Expected all column names to be renamed",
        )

    def test_get_col_names(self) -> None:
        """Test method for get_col_names."""
        col_names = MyCleaningDF.get_col_names()
        expected = tuple(MyCleaningDF.get_col_dtype_map().keys())
        assert_with_msg(
            col_names == expected,
            f"Expected col_names to be {expected}, got {col_names}",
        )

    def test_raise_on_missing_cols(self) -> None:
        """Test method for raise_on_missing_cols."""
        incomplete_map = MyCleaningDF.get_col_dtype_map()
        missing_key, _ = incomplete_map.popitem()
        missing_keys = {missing_key}

        def get_incomplete_map() -> dict[str, type[pl.DataType]]:
            return incomplete_map

        with pytest.raises(
            KeyError, match=f"{get_incomplete_map.__name__}: {missing_keys}"
        ):
            MyCleaningDF.raise_on_missing_cols(get_incomplete_map)

    def test_drop_cols(self) -> None:
        """Test method for drop_cols."""
        dirty_data = self.get_dirty_data()
        dirty_data["new_col"] = [1, 2, 3]
        c_df = MyCleaningDF(dirty_data)
        assert_with_msg(
            "new_col" not in c_df.df.columns, "Expected new_col to be dropped"
        )

        # add a col to the df attr and the call drop cols
        c_df.df = c_df.df.with_columns(pl.lit(1).alias("new_col"))
        c_df.drop_cols()
        assert_with_msg(
            "new_col" not in c_df.df.columns, "Expected new_col to be dropped"
        )

    def test_fill_nulls(self) -> None:
        """Test method for fill_nulls."""
        dirty_data = self.get_dirty_data()
        # add a null row to the dirty data
        for col in dirty_data:
            dirty_data[col].append(None)
        c_df = MyCleaningDF(dirty_data)
        # assert no nulls in the whole df
        null_counts = c_df.df.null_count()
        assert_with_msg(
            null_counts.sum_horizontal().item() == 0,
            f"Expected no nulls, got {null_counts}",
        )

        # add a null row to the df attr
        null_row = pl.DataFrame({c: [None] for c in MyCleaningDF.get_col_names()})
        c_df.df = c_df.df.vstack(null_row)
        c_df.fill_nulls()
        last_row = c_df.df.tail(1)
        # assert all the nulls are filled with the fill value
        for col, fill_value in MyCleaningDF.get_fill_null_map().items():
            last_val = last_row.select(pl.col(col)).item()
            assert_with_msg(
                last_val == fill_value,
                f"Expected {col} to be filled with {fill_value}, got {last_val}",
            )

    @pytest.mark.skip(reason="Only calls other methods")
    def test_convert_cols(self) -> None:
        """Test method for convert_cols."""

    def test_standard_convert_cols(self) -> None:
        """Test method for standard_convert_cols."""
        # add whitespace to the string col
        dirty_data = self.get_dirty_data()
        dirty_data[MyCleaningDF.STR_COL + "_old"][0] = (
            "  " + dirty_data[MyCleaningDF.STR_COL + "_old"][0] + "  "
        )
        c_df = MyCleaningDF(dirty_data)
        # assert all vals in the string col are stripped
        str_col = c_df.df.select(pl.col(MyCleaningDF.STR_COL)).to_series()
        assert_with_msg(
            all(s == s.strip() for s in str_col),
            "Expected all vals in the string col to be stripped",
        )

    def test_custom_convert_cols(self) -> None:
        """Test method for custom_convert_cols."""
        c_df = self.get_cleaning_df()
        # assert the int col is increased by 1
        before = self.get_dirty_data()[MyCleaningDF.INT_COL + "_old"]
        after = c_df.df.select(pl.col(MyCleaningDF.INT_COL)).to_series()
        # check overall sum bc of sorting
        assert_with_msg(
            after.sum() == sum(before) + len(before),
            f"Expected sum {sum(before) + len(before)}, got {after.sum()}",
        )

        # call standard convert cols and assert the int col is again increased by 1
        c_df.custom_convert_cols()
        before = after.to_list()
        after = c_df.df.select(pl.col(MyCleaningDF.INT_COL)).to_series()
        for a, b in zip(after, before, strict=True):
            assert_with_msg(
                a == b + 1, f"Expected {a} to be {b} + 1, got {a} == {b + 1}"
            )

    def test_strip_col(self) -> None:
        """Test method for strip_col."""
        # make pl.Series with some whitespace
        with_whitespace = pl.Series(["  a  ", "  b  ", "  c  "])
        # strip the whitespace
        without_whitespace = MyCleaningDF.strip_col(with_whitespace)
        # assert all vals are stripped
        assert_with_msg(
            all(s == s.strip() for s in without_whitespace),
            "Expected all vals to be stripped",
        )

    def test_lower_col(self) -> None:
        """Test method for lower_col."""
        # make pl.Series with some uppercase
        with_uppercase = pl.Series(["A", "B", "C"])
        # lower the case
        lowercase = MyCleaningDF.lower_col(with_uppercase)
        # assert all vals are lowercase
        assert_with_msg(
            all(s == s.lower() for s in lowercase), "Expected all vals to be lowercase"
        )

    def test_round_col(self) -> None:
        """Test method for round_col."""
        # make a pl.Series with some floats
        with_floats = pl.Series(
            # generate a long one with a lot of decimal places
            name=MyCleaningDF.FLOAT_COL,
            values=[
                round(i * 0.123456789, random.randint(1, 10))  # noqa: S311  # nosec: B311
                for i in range(10000)
            ],
        )
        # round the floats
        rounded = MyCleaningDF.round_col(with_floats, precision=None, compensate=True)
        # assert all vals are rounded
        assert_with_msg(
            all(s == round(s, 2) for s in rounded), "Expected all vals to be rounded"
        )
        # assert the diff in sum is smaller
        # than the smallest number possible with precision in get_col_precision_map
        precision = MyCleaningDF.get_col_precision_map()[MyCleaningDF.FLOAT_COL]
        diff = abs(with_floats.sum() - rounded.sum())
        assert_with_msg(
            diff < 10**-(precision),
            f"Expected diff to be < 10**-(precision), got {diff}",
        )

    def test_skip_col_converter(self) -> None:
        """Test method for skip_col_converter."""
        with pytest.raises(NotImplementedError):
            MyCleaningDF.skip_col_converter(pl.Series([1, 2, 3]))

    def test_drop_null_subsets(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test method for drop_null_subsets."""
        dirty_data = self.get_dirty_data()
        subsets = MyCleaningDF.get_drop_null_subsets()
        fill_null_map = MyCleaningDF.get_fill_null_map()
        for col in MyCleaningDF.get_col_names():
            for subset in subsets:
                if col in subset:
                    dirty_data[col + "_old"].append(None)
                else:
                    dirty_data[col + "_old"].append(fill_null_map[col])
        # overwrite cdf fill nulls to not overwrite the added nulls
        with monkeypatch.context() as m:
            m.setattr(MyCleaningDF, "fill_nulls", lambda _self: None)
            # overwrite standard convert cols to not get math errors when rounding
            m.setattr(MyCleaningDF, "standard_convert_cols", lambda _self: None)

            c_df = MyCleaningDF(dirty_data)
            # assert the last rows are dropped and shape is the same as before
        og_dirty_data = self.get_dirty_data()
        assert_with_msg(
            c_df.df.shape
            == (
                len(og_dirty_data[next(iter(og_dirty_data))]),
                len(MyCleaningDF.get_col_names()),
            ),
            "Expected last rows to be dropped",
        )

    def test_handle_duplicates(self, mocker: MockerFixture) -> None:
        """Test method for handle_duplicates."""
        # test if func gets called once

        spy = mocker.spy(MyCleaningDF, MyCleaningDF.handle_duplicates.__name__)
        c_df = self.get_cleaning_df()
        spy.assert_called_once_with(c_df)

        # add a duplicate row
        last_row = c_df.df.tail(1)
        c_df.df = c_df.df.vstack(last_row)
        c_df.handle_duplicates()
        # assert the last row is dropped and the values are added together
        # assert df shape is the same as before
        assert_with_msg(
            c_df.df.shape
            == (
                len(self.get_dirty_data()[next(iter(self.get_dirty_data()))]),
                len(MyCleaningDF.get_col_names()),
            ),
            "Expected df shape to be the same as before",
        )

        # order is not maintained
        # get last_row_after via string col of last row
        last_row_after = c_df.df.filter(
            pl.col(MyCleaningDF.STR_COL)
            == last_row.select(pl.col(MyCleaningDF.STR_COL)).item()
        )
        for col in MyCleaningDF.get_add_on_duplicate_cols():
            assert_with_msg(
                last_row_after.select(pl.col(col)).item()
                == last_row.select(pl.col(col)).item() * 2,
                f"Expected {col} to be added together",
            )

    def test_sort_cols(self, mocker: MockerFixture) -> None:
        """Test method for sort_cols."""
        # assert called once
        spy = mocker.spy(MyCleaningDF, MyCleaningDF.sort_cols.__name__)
        c_df = self.get_cleaning_df()
        spy.assert_called_once_with(c_df)

        # int col asc
        # subtract 1 on int col
        first_row = c_df.df.head(1)
        new_row = first_row.with_columns(
            (pl.col(MyCleaningDF.INT_COL) - 1).alias(MyCleaningDF.INT_COL),
        )
        c_df.df = c_df.df.vstack(new_row)
        c_df.sort_cols()
        # assert the first row after sort is the new row
        first_row_after = c_df.df.head(1)
        assert_with_msg(
            first_row_after.equals(new_row),
            "Expected first row to be the new row",
        )

    @pytest.mark.skip(reason="Only calls other methods")
    def test_check(self) -> None:
        """Test method for check."""

    def test_check_correct_dtypes(self, mocker: MockerFixture) -> None:
        """Test method for check_correct_dtypes."""
        spy = mocker.spy(MyCleaningDF, MyCleaningDF.check_correct_dtypes.__name__)
        c_df = self.get_cleaning_df()
        spy.assert_called_once_with(c_df)

        # change dtype of int col to float
        c_df.df = c_df.df.with_columns(pl.col(MyCleaningDF.INT_COL).cast(pl.Float64))
        with pytest.raises(TypeError):
            c_df.check_correct_dtypes()

    def test_check_no_null_cols(self, mocker: MockerFixture) -> None:
        """Test method for check_no_null_cols."""
        spy = mocker.spy(MyCleaningDF, MyCleaningDF.check_no_null_cols.__name__)
        c_df = self.get_cleaning_df()
        spy.assert_called_once_with(c_df)

        # add a null row
        new_row = pl.DataFrame({c: [None] for c in MyCleaningDF.get_col_names()})
        c_df.df = c_df.df.vstack(new_row)
        with pytest.raises(ValueError, match="Null values found in column"):
            c_df.check_no_null_cols()

    def test_check_no_nan(self, mocker: MockerFixture) -> None:
        """Test method for check_no_nan_cols."""
        spy = mocker.spy(MyCleaningDF, MyCleaningDF.check_no_nan.__name__)
        c_df = self.get_cleaning_df()
        spy.assert_called_once_with(c_df)

        # add a nan row where float col get nan and the rest the fill null value
        fill_null_map = MyCleaningDF.get_fill_null_map()
        new_row = pl.DataFrame(
            {
                c: [fill_null_map[c] if c != MyCleaningDF.FLOAT_COL else float("nan")]
                for c in MyCleaningDF.get_col_names()
            }
        )
        c_df.df = c_df.df.vstack(new_row)
        with pytest.raises(ValueError, match="NaN values found in the dataframe"):
            c_df.check_no_nan()
