"""
This is the primary testing file which will hold all the test cases
that can contribute to the student's score.
"""

import time
import unittest  # Python's unit testing library
import os  # For moving files looking inside of folders
import utils  # Our custom utility package

# All of Gradescope's special decorators to modify
# how the tests are weighted and displayed
from gradescope_utils.autograder_utils.decorators import (
    # visibility,
    weight,
    number,
    partial_credit,
    # leaderboard,
)


class Test01Setup(unittest.TestCase):
    """
    Collection of test cases used to check and move files into the correct
    location and compile the main executable.
    """

    # Files that must be in their submission
    # They will fail the first test case if they don't have these files
    required_files = ["lab04a.c", "makefile"]

    # Files that can be in their submission and should be
    # copied over. These could be extra credit files
    optional_files = []

    # If a submitted file is not a required or optional file, then
    # they will fail the first test case.
    # This helps reduce the number of extra files submitted by the student,
    # making it easier for the TAs to grade the correct files later

    # Copying all the files from the drivers folder into
    # the source directory, so we can use them to test the
    # student's code later
    # When the autograder is used, the cwd (i.e. the ".") is the
    # source directory (/autograder/source/)
    if os.path.isdir("tests/drivers") and len(os.listdir("tests/drivers")) > 0:
        os.system("cp -r tests/drivers/* .")

    @number("0.1")  # Does not affect execution order
    @weight(0)
    def test_01_check_files(self):
        """Expected files are present"""

        # Checking if the required files all exist and
        # no unexpected files were given
        # Moves the files into the source directory as well
        utils.check_and_get_files(self.required_files, self.optional_files)

        time.sleep(1)  # Gives a moment for the files to be moved over
        # and recognized by the system

    @number("0.2")
    @weight(0)
    def test_02_check_compile(self):
        """Main program compiles"""

        # Tries to compile the student's main program
        # You could use the student's makefile
        # If all you want to test is individual functions, then you
        # wouldn't need to do this because you'll be compiling your
        # own drivers instead
        _, errors = utils.subprocess_run(["make"], "student")
        # Other example:
        # output, errors = utils.subprocess_run(["g++", "main.cpp",
        #                       "object.cpp", "-Wall", "-o", "main.out"])

        # Display errors if there are any
        # Because this doesn't interact with any of our hidden drivers,
        # it's okay to show the student's output
        if errors != "":
            msg = (
                "Errors when compiling using your makefile's"
                " default directive: " + errors
            )

            # At this point, you can add extra info to the message
            # if you want to reiterate any important directions relevant to
            # passing this test case
            msg += ""
            raise AssertionError(msg)

        # What files should be created when the student's makefile is run
        files_that_should_be_created = ["MagicSquares.out"]

        not_found_message = ""
        for file in files_that_should_be_created:
            if not os.path.isfile(os.path.join(os.getcwd(), file)):
                not_found_message += (
                    f"{file} was not created with your makefile's "
                    "default directive\n"
                )

        if not_found_message != "":
            raise AssertionError(not_found_message)


class Test02Outputchecking(unittest.TestCase):
    def setUp(self):
        self.submission1 = utils.run_program("MagicSquares.out",
                                                txt_contents="1 2 3 4 5 6 7 8 9\n")
        self.submission2 = utils.run_program("MagicSquares.out",
                                                txt_contents="4 9 2 3 5 7 8 1 6\n")

    @number("1.1")
    @weight(1)

    def test_11_general_outputs(self):
        """Common flow outputs are correct"""
        expected_phrases = ["Enter in the values:", "You entered:", "Analyzing..."]
        
        missing = utils.phrases_out_of_order(expected_phrases, self.submission1.output)
        msg = "" 
        for i in missing:
            msg += f"Couldn't find: {expected_phrases[i]}\n"

        if msg != "":
            raise AssertionError(msg)

    @number("1.2")
    @weight(1)

    def test_12_square_output(self):
        """Inputted numbers are displayed as a square correctly"""
        square = "1 2 3\n4 5 6\n7 8 9\n"
        if square not in self.submission1.output:
            raise AssertionError("Square is incorrect or missing\n" "Make sure there are no extra spaces")
        
    @number("1.3")
    @weight(1)
    def test_13_not_square_outputs(self):
        """Not Magic Square identified correctly"""
        expected_phrases = ["[1, 2, 3] does not work!]",  
                            "[7, 8, 9] does not work!",
                            "Column 0 does not work!",
                            "Column 2 does not work!",
                            "This is not a magic square!"]
        msg = ""
        for phrase in expected_phrases:
            if phrase not in self.submission1.output:
                msg += f"Phrase not found: '{phrase}'\n"

    @number("1.4")
    @weight(1)
    def test_14_square_outputs(self):
        """Magic Square identified correctly"""
        wrong = False
        if "This is a magic square!" not in self.submission2.output:
            wrong = True

        if "This is not a magic square!" in self.sumbission2.output:
            wrong = True
        
        if wrong:
            raise AssertionError("Square was not correctly identified as a magic square")

        




