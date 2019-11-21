import os
import string
import unittest
import tempfile
from random import randint, choice, getrandbits

import pybloomfilter

from tests import with_test_file


class SimpleTestCase(unittest.TestCase):
    FILTER_SIZE = 200
    FILTER_ERROR_RATE = 0.001

    def setUp(self):
        # Convenience file-backed bloomfilter
        self.tempfile = tempfile.NamedTemporaryFile(suffix='.bloom',
                                                    delete=False)
        self.bf = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                            self.FILTER_ERROR_RATE,
                                            self.tempfile.name)

        # Convenience memory-backed bloomfilter
        self.bf_mem = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                                self.FILTER_ERROR_RATE)

    def tearDown(self):
        os.unlink(self.tempfile.name)

    def assertPropertiesPreserved(self, old_bf, new_bf):
        # Assert that a "new" BloomFilter has the same properties as an "old"
        # one.
        failures = []
        for prop in ['capacity', 'error_rate', 'num_hashes', 'num_bits',
                     'hash_seeds']:
            old, new = getattr(old_bf, prop), getattr(new_bf, prop)
            if new != old:
                failures.append((prop, old, new))
        self.assertEqual([], failures)

    def _random_str(self, length=16):
        chars = string.ascii_letters
        return ''.join(choice(chars) for _ in range(length))

    def _random_set_of_stuff(self, c):
        """
        Return a random set containing up to "c" count of each type of Python
        object.
        """
        return set(
            # Due to a small chance of collision, there's no guarantee on the
            # count of elements in this set, but we'll make sure that's okay.
            [self._random_str() for _ in range(c)] +
            [randint(-1000, 1000) for _ in range(c)] +
            [(randint(-200, 200), self._random_str()) for _ in range(c)] +
            [float(randint(10, 100)) / randint(10, 100)
             for _ in range(c)] +
            [int(randint(50000, 1000000)) for _ in range(c)] +
            [object() for _ in range(c)] +
            [str(self._random_str) for _ in range(c)])

    def _populate_filter(self, bf, use_update=False):
        """
        Populate given BloomFilter with a handfull of hashable things.
        """
        self._in_filter = self._random_set_of_stuff(10)
        self._not_in_filter = self._random_set_of_stuff(15)
        # Just in case we randomly chose a key which was also in
        # self._in_filter...
        self._not_in_filter = self._not_in_filter - self._in_filter

        if use_update:
            bf.update(self._in_filter)
        else:
            for item in self._in_filter:
                bf.add(item)

    def _check_filter_contents(self, bf):
        for item in self._in_filter:
            # We should *never* say "not in" for something which was added
            self.assertTrue(item in bf, '%r was NOT in %r' % (item, bf))

        # We might say something is in the filter which isn't; we're only
        # trying to test correctness, here, so we are very lenient.  If the
        # false positive rate is within 2 orders of magnitude, we're okay.
        false_pos = len(list(filter(bf.__contains__, self._not_in_filter)))
        error_rate = float(false_pos) / len(self._not_in_filter)
        self.assertTrue(error_rate < 100 * self.FILTER_ERROR_RATE,
                        '%r / %r = %r > %r' % (false_pos,
                                               len(self._not_in_filter),
                                               error_rate,
                                               100 * self.FILTER_ERROR_RATE))
        for item in self._not_in_filter:
            # We should *never* have a false negative
            self.assertFalse(item in bf, '%r WAS in %r' % (item, bf))

    def test_repr(self):
        self.assertEqual(
            '<BloomFilter capacity: %d, error: %0.3f, num_hashes: %d>' % (
                self.bf.capacity, self.bf.error_rate, self.bf.num_hashes),
            repr(self.bf))
        self.assertEqual(
            '<BloomFilter capacity: %d, error: %0.3f, num_hashes: %d>' % (
                self.bf.capacity, self.bf.error_rate, self.bf.num_hashes),
            str(self.bf))
        self.assertEqual(
            '<BloomFilter capacity: %d, error: %0.3f, num_hashes: %d>' % (
                self.bf.capacity, self.bf.error_rate, self.bf.num_hashes),
            str(self.bf))

    def test_add_and_check_file_backed(self):
        self._populate_filter(self.bf)
        self._check_filter_contents(self.bf)

    def test_update_and_check_file_backed(self):
        self._populate_filter(self.bf, use_update=True)
        self._check_filter_contents(self.bf)

    def test_add_and_check_memory_backed(self):
        self._populate_filter(self.bf_mem)
        self._check_filter_contents(self.bf_mem)

    def test_open(self):
        self._populate_filter(self.bf)
        self.bf.sync()

        bf = pybloomfilter.BloomFilter.open(self.bf.name.decode())
        self._check_filter_contents(bf)

    @with_test_file
    def test_readonly(self, filename):
        bf = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                       self.FILTER_ERROR_RATE,
                                       filename)
        self._populate_filter(bf)
        self._check_filter_contents(bf)
        self.assertEqual(bf.read_only, False)
        bf.sync()

        bfro = pybloomfilter.BloomFilter.open(filename, mode="r")
        self._check_filter_contents(bfro)
        self.assertEqual(bfro.read_only, True)

    def test_readonly_cannot_write(self):
        bfro = pybloomfilter.BloomFilter.open(self.tempfile.name, mode="r")
        self.assertRaises(ValueError, bfro.add, "test")
        self.assertRaises(ValueError, bfro.update, ["test"])
        self.assertRaises(ValueError, bfro.sync)
        self.assertRaises(ValueError, bfro.clear_all)

    def test_readonly_cannot_do_set_operations(self):
        bf_mem = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                           self.FILTER_ERROR_RATE)

        bfro = pybloomfilter.BloomFilter.open(self.tempfile.name, mode="r")
        self.assertRaises(ValueError, bfro.union, bf_mem)

        bfro = pybloomfilter.BloomFilter.open(self.tempfile.name, mode="r")
        self.assertRaises(ValueError, bfro.intersection, bf_mem)

        bfro = pybloomfilter.BloomFilter.open(self.tempfile.name, mode="r")
        self.assertRaises(ValueError, bfro.__ior__, bf_mem)

        bfro = pybloomfilter.BloomFilter.open(self.tempfile.name, mode="r")
        self.assertRaises(ValueError, bfro.__iand__, bf_mem)

    @with_test_file
    def test_copy(self, filename):
        self._populate_filter(self.bf)
        self.bf.sync()

        bf = self.bf.copy(filename)
        self._check_filter_contents(bf)
        self.assertPropertiesPreserved(self.bf, bf)

    def assertBfPermissions(self, bf, perms):
        oct_mode = oct(os.stat(bf.name).st_mode)
        self.assertTrue(oct_mode.endswith(perms),
                     'unexpected perms %s' % oct_mode)

    @with_test_file
    def test_to_from_base64(self, filename):
        self._populate_filter(self.bf)
        self.bf.sync()

        # sanity-check
        self.assertBfPermissions(self.bf, '0755')

        b64 = self.bf.to_base64()

        old_umask = os.umask(0)
        try:
            os.unlink(filename)
            bf = pybloomfilter.BloomFilter.from_base64(filename, b64,
                                                       perm=0o775)
            self.assertBfPermissions(bf, '0775')
            self._check_filter_contents(bf)
            self.assertPropertiesPreserved(self.bf, bf)
        finally:
            os.umask(old_umask)

    def test_missing_file_is_os_error(self):
        self.assertRaises(OSError, pybloomfilter.BloomFilter, 1000, 0.1,
                          'missing_directory/some_file.bloom')

    @with_test_file
    def test_others(self, filename):
        bf = pybloomfilter.BloomFilter(100, 0.01, filename)
        for elem in (1.2, 2343, (1, 2), object(), '\u2131\u3184'):
            bf.add(elem)
            self.assertEqual(elem in bf, True)

    def test_number_nofile(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        bf.add(1234)
        self.assertEqual(1234 in bf, True)

    def test_string_nofile(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        bf.add("test")
        self.assertEqual("test" in bf, True)

    def test_others_nofile(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        for elem in (1.2, 2343, (1, 2), object(), '\u2131\u3184'):
            bf.add(elem)
            self.assertEqual(elem in bf, True)

    @with_test_file
    def _test_large_file(self, filename):
        bf = pybloomfilter.BloomFilter(400000000, 0.01, filename)
        bf.add(1234)
        self.assertEqual(1234 in bf, True)

    def test_name_does_not_segfault(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        self.assertRaises(NotImplementedError, lambda: bf.name)

    def test_copy_does_not_segfault(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        with tempfile.NamedTemporaryFile(suffix='.bloom') as f2:
            self.assertRaises(NotImplementedError, bf.copy, f2.name)

    def test_to_base64_does_not_segfault(self):
        bf = pybloomfilter.BloomFilter(100, 0.01)
        self.assertRaises(NotImplementedError, bf.to_base64)

    def test_ReadFile_is_public(self):
        self.assertEqual(
            isinstance(pybloomfilter.BloomFilter.ReadFile, object), True)
        bf = pybloomfilter.BloomFilter(100, 0.01)
        bf2 = pybloomfilter.BloomFilter(100, 0.01)
        self.assertEqual(bf.ReadFile, bf2.ReadFile)
        self.assertEqual(pybloomfilter.BloomFilter.ReadFile,
                          bf.ReadFile)

    def test_copy_template(self):
        self._populate_filter(self.bf)
        with tempfile.NamedTemporaryFile() as _file:
            bf2 = self.bf.copy_template(_file.name)
            self.assertPropertiesPreserved(self.bf, bf2)
            bf2.union(self.bf)  # Asserts copied bloom filter is comparable
            self._check_filter_contents(bf2)

    def test_create_with_hash_seeds(self):
        cust_seeds = [getrandbits(32) for i in range(30)]
        bf = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                       self.FILTER_ERROR_RATE,
                                       self.tempfile.name,
                                       hash_seeds=cust_seeds)
        bf_seeds = bf.hash_seeds.tolist()
        self.assertEqual(cust_seeds, bf_seeds)

    def test_create_with_hash_seeds_invalid(self):
        cust_seeds = ["ABC", -123, "123456", getrandbits(33)]
        self.assertRaises(ValueError,
                          pybloomfilter.BloomFilter,
                          self.FILTER_SIZE,
                          self.FILTER_ERROR_RATE,
                          hash_seeds=cust_seeds)

    def test_create_with_hash_seeds_and_compare(self):
        test_data = "test"
        bf1 = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                        self.FILTER_ERROR_RATE,
                                        self.tempfile.name)
        bf1.add(test_data)
        bf1_seeds = bf1.hash_seeds.tolist()
        bf1_base64 = bf1.to_base64()
        bf1.close()

        bf2 = pybloomfilter.BloomFilter(self.FILTER_SIZE,
                                        self.FILTER_ERROR_RATE,
                                        self.tempfile.name,
                                        hash_seeds=bf1_seeds)
        bf2.add(test_data)
        bf2_seeds = bf2.hash_seeds.tolist()
        bf2_base64 = bf2.to_base64()
        bf2.close()

        self.assertEqual(bf1_seeds, bf2_seeds)
        self.assertEqual(bf1_base64, bf2_base64)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleTestCase))
    return suite
