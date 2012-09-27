#!/bin/sh

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/collective.z3cform.norobots.pot --merge locales/manual.pot --create collective.z3cform.norobots .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/collective.z3cform.norobots.pot locales/*/LC_MESSAGES/collective.z3cform.norobots.po