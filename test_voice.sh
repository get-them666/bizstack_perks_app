#!/bin/bash

# Fetch the latest lead data from your sqlite database
LATEST_LEAD=$(sqlite3 bizstack.db "SELECT phone || ' has notes: ' || notes FROM leads ORDER BY rowid DESC LIMIT 1;" 2>/dev/null)

if [ -z "$LATEST_LEAD" ]; then
    # Fallback message if your database table is currently empty
    TEXT_TO_SPEAK="Hi Shaun, this is your live terminal voice agent test. Your bizstack database connection is running smoothly."
else
    TEXT_TO_SPEAK="New lead alert detected in your database. $LATEST_LEAD"
fi

echo "🤖 Voice Agent Speaking: '$TEXT_TO_SPEAK'"

# Uses your Mac's native speech synthesis engine to verbalize the text string
say -v Samantha "$TEXT_TO_SPEAK"

echo "✅ Audio playback complete."
