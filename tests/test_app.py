import unittest,app
class ManifestTests(unittest.TestCase):
 def test_missing_fields(self):
  r=app.validate({"name":"Demo","start_url":"/","display":"standalone","icons":[]})
  self.assertGreaterEqual(r["warnings"],1)
 def test_good_minimal(self):
  r=app.validate({"name":"Demo","start_url":"/","display":"standalone","icons":[{"src":"/icon.png","sizes":"192x192","type":"image/png"}]})
  self.assertEqual(r["errors"],0)
if __name__=="__main__":unittest.main()
