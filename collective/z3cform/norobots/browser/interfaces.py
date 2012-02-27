from zope.interface import Interface


class INorobotsView(Interface):
    """Norobots question generating and verifying view

    Usage:

        - Use the view from a page to get a question. Use the 'get_question' method.

        - The user will answer the question, and tell the server through a form
          submission.

        - Use the user input to verify.
    """

    def get_question():
        """Return a random question: {'id': '...', 'title': '...', 'id_check': '...'}"""

    def verify(input, question_id, id_check):
        """Verify the user-supplied input for a question id and is corresponding id_check.

        Returns a boolean value indicating if the input matched
        """
