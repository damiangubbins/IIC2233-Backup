import sys
import unittest

# Advertencia, la siguiente línea solo es utiliza por el cuerpo docente.
# Se considerará una mala práctica ocuparlo en sus evaluaciones.
sys.path.append("..")

from funciones_servidor import codificar_mensaje


class TestCodificarMensaje(unittest.TestCase):

    def test_0(self):
        mensaje = bytearray(b"Hola Mundo")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\n"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(b"Hola Mundo\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        ])

    def test_1(self):
        mensaje = bytearray(b"\xc2\xb4+{}[]\xc2\xa8*!#$%&/()")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x12"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(b"\xc2\xb4+{}[]\xc2\xa8*!#$%&/()\x00\x00\x00\x00\x00\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_2(self):
        mensaje = bytearray(b"A\xc3\xb1o nuevo, vida nueva")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x16"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(
                b"A\xc3\xb1o nuevo, vida nueva\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00"),
        ])

    def test_3(self):
        mensaje = bytearray(
            b"\xc3\xb1a\xc3\xb1e\xc3\xb1i\xc3\xb1d\xc3\xb1r\xc3\xb1t\xc3"
            b"\xb1ch\xc3\xb1h\xc3\xb1l\xc3\xb1\xc3\xb1\xc2\xb4\xc2\xb4"
            b"\xc3\xb1\xc3\xb1\xc2\xb4\xc2\xb4\xc3\xb1")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00."),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(
                b"\xc3\xb1a\xc3\xb1e\xc3\xb1i\xc3\xb1d\xc3\xb1r\xc3"
                b"\xb1t\xc3\xb1ch\xc3\xb1h\xc3\xb1l\xc3\xb1\xc3\xb1\xc2\xb4\xc2\xb4"),
            bytearray(b"\x00\x00\x00\x02"),
            bytearray(b"\xc3\xb1\xc3\xb1\xc2\xb4\xc2\xb4\xc3\xb1\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_4(self):
        mensaje = bytearray(
            b"{}\xc2\xb4+[]\xc2\xa8*^`\xc2\xa8~\'\xc2\xbf?\xc2\xa1\\\xc2"
            b"\xb8\xc2\xa8*^`\xc2\xa8~\'\xc2\xbf?\xc2\xa1\\\xc2\xb8|\xc2\xb0"
            b"\xc2\xac!#$%&/()=|@\xc2\xb7~\xc2\xbd\xc2\xac{[]}")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00D"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(
                b"{}\xc2\xb4+[]\xc2\xa8*^`\xc2\xa8~\'\xc2"
                b"\xbf?\xc2\xa1\\\xc2\xb8\xc2\xa8*^`\xc2\xa8~\'\xc2\xbf?"),
            bytearray(b"\x00\x00\x00\x02"),
            bytearray(
                b"\xc2\xa1\\\xc2\xb8|\xc2\xb0\xc2\xac!#$%&/()=|@\xc2"
                b"\xb7~\xc2\xbd\xc2\xac{[]}\x00\x00\x00\x00"),
        ])

    def test_5(self):
        mensaje = bytearray(
            b"\xe2\x80\xa1\xe2\x80\xa0\xc6\x92\xe2\x82\xac\xe2\x80\xb0\xc5\xa0\xc5\x92\xc5\xbd")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x14"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(b"\xe2\x80\xa1\xe2\x80\xa0\xc6\x92\xe2\x82"
                      b"\xac\xe2\x80\xb0\xc5\xa0\xc5\x92\xc5\xbd\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_6(self):
        mensaje = bytearray(b"   ")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x03"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(b"   \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                      b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_7(self):
        mensaje = bytearray(b"1 1 1 1 1 1 1 1 1 1 1 1")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x17"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(
                b"1 1 1 1 1 1 1 1 1 1 1 1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_8(self):
        mensaje = bytearray(b"abcdefghijklmnopqrstuvwxyz")
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\x00\x1a"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(
                b"abcdefghijklmnopqrstuvwxyz\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])

    def test_9(self):
        mensaje = bytearray(b"1"*10000)
        respuesta = codificar_mensaje(mensaje)
        self.assertIsInstance(respuesta, list)
        for i in respuesta:
            self.assertIsInstance(i, bytearray)
        self.assertEqual(respuesta, [
            bytearray(b"\x00\x00\'\x10"),
            bytearray(b"\x00\x00\x00\x01"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x02"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x03"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x04"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x05"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x06"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x07"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x08"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\t"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\n"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x0b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x0c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\r"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x0e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x0f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x10"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x11"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x12"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x13"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x14"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x15"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x16"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x17"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x18"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x19"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1a"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1d"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x1f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00 "),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00!"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\""),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00#"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00$"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00%"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00&"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\'"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00("),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00)"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00*"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00+"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00,"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00-"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00."),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00/"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x000"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x001"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x002"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x003"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x004"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x005"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x006"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x007"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x008"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x009"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00:"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00;"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00<"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00="),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00>"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00?"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00@"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00A"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00B"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00C"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00D"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00E"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00F"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00G"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00H"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00I"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00J"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00K"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00L"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00M"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00N"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00O"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00P"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00Q"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00R"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00S"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00T"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00U"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00V"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00W"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00X"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00Y"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00Z"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00["),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\\"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00]"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00^"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00_"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00`"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00a"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00d"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00g"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00h"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00i"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00j"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00k"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00l"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00m"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00n"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00o"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00p"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00q"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00r"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00s"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00t"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00u"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00v"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00w"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00x"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00y"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00z"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00{"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00|"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00}"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00~"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x7f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x80"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x81"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x82"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x83"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x84"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x85"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x86"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x87"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x88"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x89"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8a"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8d"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x8f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x90"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x91"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x92"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x93"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x94"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x95"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x96"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x97"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x98"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x99"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9a"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9d"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\x9f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xa9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xaa"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xab"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xac"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xad"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xae"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xaf"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xb9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xba"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xbb"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xbc"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xbd"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xbe"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xbf"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xc9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xca"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xcb"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xcc"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xcd"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xce"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xcf"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xd9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xda"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xdb"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xdc"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xdd"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xde"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xdf"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xe9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xea"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xeb"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xec"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xed"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xee"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xef"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf0"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf1"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf2"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf3"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf4"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf5"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf6"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf7"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf8"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xf9"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xfa"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xfb"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xfc"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xfd"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xfe"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x00\xff"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x00"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x01"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x02"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x03"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x04"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x05"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x06"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x07"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x08"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\t"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\n"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x0b"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x0c"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\r"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x0e"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x0f"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x10"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x11"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x12"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x13"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x14"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x15"),
            bytearray(b"111111111111111111111111111111111111"),
            bytearray(b"\x00\x00\x01\x16"),
            bytearray(
                b"1111111111111111111111111111\x00\x00\x00\x00\x00\x00\x00\x00"),
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
