#!/bin/bash
celery -A night_owl_market worker -Q msg_to_db,msg_to_group -l info