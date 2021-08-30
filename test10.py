class Test10:
    def test_check_length(self):

        phrase = input("Set a your phrase: ")
        assert len(phrase) < 15, "Длина фразы больше или равна 15 символам"

