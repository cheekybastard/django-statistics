from datetime import datetime, timedelta, date
from django import template
from django.template.defaultfilters import stringfilter
from statistics.models import *
import logging

register = template.Library()


class VisitHistory(template.Node):
    def __init__(self, var_name):
        self.varname = var_name

    def render(self, context):
        try:
            total = Visit.objects.all()
        except Exception, e:
            logging.error(e)
            total = []
        context[self.varname] = total
        return ''

@register.tag
def get_visit_history(parser, token):
    "Return all visits"
    try:
        tag_name, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    #print "Tag: %s -- Var: %s -- User: %s" % (tag_name, var_name, user_name)
    return VisitHistory(var_name)

# USAGE
# {% get_visit_history total %}
# {{ total }}  -> return total visit


class VisitHistorySum(template.Node):
    def __init__(self, var_name):
        self.varname = var_name

    def render(self, context):
        try:
            year = datetime.datetime.now().year
            results = StatisticsMonthYear.objects.filter(anno=year)
            #mesi = Months.objects.all()
            January = 0
            February = 0
            March = 0
            April = 0
            May = 0
            June = 0
            July = 0
            August = 0
            September = 0
            October = 0
            November = 0
            December = 0
            for i in results:
                if i.mese.nome == "January": January += i.number
                if i.mese.nome == "February": February += i.number
                if i.mese.nome == "March": March += i.number
                if i.mese.nome == "April": April += i.number
                if i.mese.nome == "May": May += i.number
                if i.mese.nome == "June": June += i.number
                if i.mese.nome == "July": July += i.number
                if i.mese.nome == "August": August += i.number
                if i.mese.nome == "September": September += i.number
                if i.mese.nome == "October": October += i.number
                if i.mese.nome == "November": November += i.number
                if i.mese.nome == "December": December += i.number
            #logging.error("MESI %s %s %s %s %s %s %s %s %s", Gennaio, Febbraio, Marzo, Aprile, Maggio, Giugno, Luglio, Agosto, Settembre)
            results = [("January", January),("February", February),("March", March),("April", April),("May", May),("June", June),("July", July),("August", August),("September", September),("October", October),("November", November),("December", December)]
            #logging.error(results)
        except Exception, e:
            logging.error(e)
            results = []
        #logging.error("RES %s",results)
        context[self.varname] = results
        return ''

@register.tag
def get_visit_history_sum(parser, token):
    "Return all visits"
    try:
        tag_name, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    #print "Tag: %s -- Var: %s -- User: %s" % (tag_name, var_name, user_name)
    return VisitHistorySum(var_name)

# USAGE
# {% get_visit_history_sum total %}
# {{ total }}  -> return total sum visit in graph

