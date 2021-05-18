import unittest

from opencensus.ext.masker import masker


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        masker.masked_fields(('hidden',))
        masker.masked_params(('hidden_param',))

    def test_mask_dict(self):
        expected = '{"hello": "Hola", "hidden": "************"}'
        actual = masker.mask_fields({'hello': 'Hola', 'hidden': 'Masked field'})
        self.assertEqual(expected, actual)

    def test_mask_dict_indented(self):
        expected = '{"parent": {"child": {"hello": "Hola", "hidden": "************"}}}'
        actual = masker.mask_fields({'parent': {'child': {'hello': 'Hola', 'hidden': 'Masked field'}}})
        self.assertEqual(expected, actual)

    def test_mask_list(self):
        expected = '[{"hello": "Hola"}, {"hidden": "************"}]'
        actual = masker.mask_fields([{'hello': 'Hola'}, {'hidden': 'Masked field'}])
        self.assertEqual(expected, actual)

    def test_mask_params(self):
        expected = '{"params": [{"id": "hidden_param", "value": "******"}]}'
        actual = masker.mask_params({'params': [{'id': 'hidden_param', 'value': 'Hidden'}]})
        self.assertEqual(expected, actual)

    def test_mask_params_indented(self):
        expected = '{"request": {"asset": {"params": [{"id": "hidden_param", "value": "******"}]}}}'
        actual = masker.mask_params({'request': {'asset': {'params': [{'id': 'hidden_param', 'value': 'Hidden'}]}}})
        self.assertEqual(expected, actual)

    def test_mask_config_param(self):
        expected = '{"parameter": {"id": "hidden_param", "value": "******"}, "value": "**************"}'
        actual = masker.mask_params({'parameter': {'id': 'hidden_param', 'value': 'Hidden'}, 'value': 'Another hidden'})
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
