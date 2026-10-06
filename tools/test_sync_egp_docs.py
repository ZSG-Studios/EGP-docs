"""Regression checks for public declarations, default values and scope."""

import unittest

from sync_egp_docs import public_types


class DeclarationTests(unittest.TestCase):
    def test_multiline_csharp_method_and_property(self):
        source = """
        public sealed class Prediction {
            public int PendingTicks => native.Call("pending").AsInt32();
            public Error Configure(Func<byte[]> capture,
                Func<long, byte[], bool, Error> simulate, int maxTicks = 128)
                => Invoke(capture, simulate, maxTicks);
            public int Limit { get; set; } = 128;
        }
        """
        declaration = dict(public_types(source, False))["Prediction"]
        self.assertIn("Func<long, byte[], bool, Error> simulate, int maxTicks = 128);", declaration)
        self.assertIn("public int PendingTicks { get; }", declaration)
        self.assertIn("public int Limit { get; set; } = 128;", declaration)
        self.assertNotIn("Invoke", declaration)
        self.assertNotIn("native.Call", declaration)

    def test_cpp_visibility_braced_default_and_constructor(self):
        source = """
        namespace egp::networking {
        namespace detail { class Hidden { public: void leak() {} }; }
        class Session {
            Ref<Value> native;
        public:
            Session() : native(make_value("} {")) {}
            Error configure(const Options &options = {}) { return OK; }
            Error track(int64_t entity, int64_t body_id = 0) { return OK; }
        private:
            void helper() {}
        };
        }
        """
        declarations = dict(public_types(source, True))
        self.assertEqual(set(declarations), {"Session"})
        declaration = declarations["Session"]
        self.assertIn("public:", declaration)
        self.assertIn("Session();", declaration)
        self.assertIn("Error configure(const Options &options = {});", declaration)
        self.assertIn("Error track(int64_t entity, int64_t body_id = 0);", declaration)
        self.assertNotIn("native", declaration)
        self.assertNotIn("helper", declaration)

    def test_internal_csharp_type_is_excluded(self):
        source = """
        internal class Hidden { public void Dispose() {} }
        public readonly record struct Result(Error Error, long Entity);
        public enum Delivery { Reliable = 2, Unreliable = 4 }
        """
        self.assertEqual(set(dict(public_types(source, False))), {"Result", "Delivery"})

    def test_string_default_whitespace_is_retained(self):
        source = """namespace egp::networking {
        struct Options { String protocol = "game  protocol"; };
        }"""
        self.assertIn('"game  protocol"', dict(public_types(source, True))["Options"])


if __name__ == "__main__":
    unittest.main()
