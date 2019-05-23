from drugscom import drugscom
# from drugscom_package.application import application
# from drugscom_package.drugscom_manager import drugscom_manager
import json
import time
import sys
import psycopg2

def get_from_color_name(color,color_codes) -> int:
    colors = color.split(";")
    for i in range(len(colors)):
        if len(colors) == 2:
            color = colors[i][0] + colors[i][1:].lower() + " & " + \
                    colors[1 if i == 0 else 0][0] + colors[1 if i == 0 else 0][1:].lower()
        else:
            color = color[0] + color[1:].lower()
        for d in color_codes:
            if d["name"] == color:
                return d["id"]
    print(f"unknown color name {color} ")
    return 12  # white

def get_from_shape_name(shape,shape_codes) ->int:
    shape = shape[0] + shape[1:].lower()
    for d in shape_codes:
        if d["name"] == shape:
            return d["id"]
    print(f"unknown shape name {shape} ")
    return 0 # Round   

def main():
    # run_test()
    # return
    d = drugscom()
    connection = psycopg2.connect(user = "mark", password="p", dbname="rxidDS")
    # connection = psycopg2.connect(user = "obpcyvjlcuatjs",
    #                                 password = "5aa89d47aef2552275e120d574f188b6b5cb854c88c543c8c6b215dfcfae5da4",
    #                                 host = "ec2-54-197-232-203.compute-1.amazonaws.com",
    #                                 dbname = "d3749ifkbn31o0")
    print("connection is None:", connection == None)
    cur = connection.cursor()
    # cur.execute(
    #     f"""UPDATE rxid.rxid_meds_data
    #         SET side_effects = "",
    #         dmprint = "dp 331",
    #         dbrand = "Kariva inert"
    #         WHERE "ID" = {id};""".strip())
    # connection.commit()    
    # x = "test side_effects"
    # x2 = "2nd update"
    # cur.execute(
    #             f"""UPDATE rxid.rxid_meds_data
    #                 SET side_effects = "{x}"
    #                 WHERE "ID" = 27323;""".strip())
    # connection.commit() 
    # cur.execute(
    #             f"""UPDATE rxid.rxid_meds_data
    #                 SET side_effects = "{x2}"
    #                 WHERE "ID" = 27324;""".strip())
    # connection.commit() 
    # return
    cur.execute("""SELECT count(*) FROM rxid.rxid_meds_data;""" )
    row = cur.fetchall()[0]
    # for row in rows:
    #     print (f"  {row[0]}")
    row_count = int(row[0])
    print("row_count", row_count)
    id = -1
    cur.execute("SELECT splshape_text,splcolor_text, splimprint, "ID", side_effects FROM rxid.rxid_meds_data;")
    rows = cur.fetchall()
    # row = None
    row_number = 1
    for row in rows:
        # try:
        #     # cur.execute(f"""
        #     #         SELECT splshape_text,splcolor_text, splimprint, "ID", side_effects
        #     #         FROM rxid.rxid_meds_data LIMIT 1 OFFSET {row_number};
        #     #         """)
        #     print("fetchone")
        #     row = cur.fetchone()
        #     if row == None:
        #         break
        # except:
        #     connection.rollback()
        #     cur = connection.cursor()
        #     continue
        # row = cur.fetchall()[0]
        if int(row[3]) == id:
            continue
        if len(row[4]) > 0: # already wrote side_effects
            continue
        id = int(row[3])
        mprint = row[2]
        if mprint == None:
            mprint=""
        shape_code = get_from_shape_name(row[0],d.shape_codes)
        color_code = get_from_color_name(row[1],d.color_codes)
        print(f"shape_code: {shape_code} for {row[0]}, color_code: {color_code} for {row[1]} ")
        print("imprint",mprint.replace(";"," ").strip(), row[2], "id", row[3], "row_number:", row_number)
        try:
            test = json.loads(d.get_data({"imprint": mprint.replace(";"," ").strip(), "color": color_code,
                    "shape": shape_code}))
            d.reset()
            
            if test != None:
                print("test",test[0], type(test[0]))
                test = test[0]
                # print("starting update")
            else:
                print("None test")
                continue
            print(f"""dmprint: "{test["dmprint"]}"""")
            cur.execute(
                f"""UPDATE rxid.rxid_meds_data
                    SET side_effects = "{test["side_effects"]}",
                    dmprint = "{test["dmprint"]}",
                    dbrand = "{test["brand"]}"
                    WHERE "ID" = {id};""".strip())
            connection.commit()
            print("update/commit worked")
            if row_number % 10 == 0:
                print("row_number",row_number,end=" ")
            row_number += 1
            # return

# UPDATE [ ONLY ] table SET
#        column = expression [, ...]
#        [ FROM source ]
#        [ WHERE condition ]
# side_effects 

        except Exception as e:
                print("error", repr(e))
                print(f"Update Error on line {sys.exc_info()[-2]}")
        # finally:
        #     print("closing")
        #     if d != None:
        #         d.close()
        #         del d
        #     return
    if d != None:
        d.close()
        del d       
        # print(f"{rows}")
        print("returning")
        return

def run_test():
    d = drugscom()
    a = None
    try:    
        # a = application.

        # print(d.color_shape_match("yellow", "yellow", "oval", "elliptical / oval"))
#{"imprint": "120 mg Andrx 696", "color": 11, "shape": 1

        # test = d.get_data({"imprint": "SON 151 4 mg", "color": 15, "shape": 1}) # white capsule
        test = d.get_data({"imprint": "H 183", "color": 11, "shape": 0}) # white capsule
        # test = d.get_data({"imprint": "M T6", "color": 12, "shape": 0}) # purple round
        # test = d.get_data({"imprint" : "Logo 4870 12.5 mg",  "color" : 15,  "shape" : 1})  # white capsule
        # test = d.get_data({"imprint" : "C 10",  "color" : 16,  "shape" : 9})  # yellow egg
        # test = d.get_data({"imprint": "Andrx 696 120 mg", "color": 11, "shape": 1}) # pink capsule
        # test = d.get_data({"imprint": "Westward 480","color": 15,"shape": 0}) # white round
        # test = d.get_data({"imprint": "SINGULAIR MSD 117", "color": 3, "shape": 19})
        # test = d.get_data({"imprint": "4mg WATSON 151", "color": 15, "shape": 1}) # white capsule
        # test = d.get_data({"imprint": "T6 M ", "color": 12, "shape": 0}) # purple round
        # test = d.get_data({"imprint" : "12.5mg 4870 ",  "color" : 15,  "shape" : 1})  # white capsule
        # test = d.get_data({"imprint" : "10 C",  "color" : 16,  "shape" : 3})  # yellow egg
        # test = d.get_data({"imprint": "120 mg Andrx 696", "color": 11, "shape": 1}) # pink capsule
        # test = d.get_data({"imprint": "480 Westward","color": 15,"shape": 0}) # white round  
        # test = d.get_data({"imprint": "MSD 117 SINGULAIR", "color": 3, "shape": 19})      
  
        # d.get_data("M Amphet Salts 30 mg")
        # test = d.get_data("BAYER 20")
        # test = d.get_data("BAYER 10")
        # test = d.get_data("M T6")
        # test = d.get_data("2876")
        # print(json.dumps(test))
        print(test)
    except Exception as e:
            print("error", repr(e))
            print(f"__main__ Error  {sys.exc_info()}")
    finally:
        if d != None:
            d.close()
            del d



if __name__ == "__main__":
    main()

