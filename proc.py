#!/usr/bin/env python3


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def main():
    first = True

    print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries, affected_states,
    affected_cities, affected_regions, influencer) values""")

    with open("data.txt", "r") as f:
        next(f)  # skip header row
        for line in f:
            focus_area, grantee, support_type, years, description = line[:-1].split("\t")
            donation_date = years[:4] + "-01-01"

            if focus_area == "Criminal Justice Reform":
                url = "https://www.futurejusticefund.org/criminaljustice"
                influencer = "Chloe Cockburn"
                focus_area = "Criminal justice reform"
                affected_countries = "United States"
            else:
                url = "https://www.futurejusticefund.org/incomesecurity"
                if grantee == "GiveDirectly":
                    focus_area = "Cash transfers"
                    affected_countries = "Kenya"
                else:
                    affected_countries = ""
                influencer = ""

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Future Justice Fund"),  # donor
                mysql_quote(grantee),  # donee
                "NULL",  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(focus_area),  # cause_area
                mysql_quote(url),  # url
                mysql_quote(url),  # donor_cause_area_url
                mysql_quote("For " + support_type + "." if support_type else ""),  # notes
                mysql_quote(affected_countries),  # affected_countries
                mysql_quote(""),  # affected_states
                mysql_quote(""),  # affected_cities
                mysql_quote(""),  # affected_regions
                mysql_quote(influencer),  # influencer
            ]) + ")")
            first = False
        print(";")


if __name__ == "__main__":
    main()
