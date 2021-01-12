import os
from flask import json
# from app import app
from bird import Bird


class ResetData():
    def __init__(self, app, session):
        self.app = app
        self.session = session
        
    def reset_data(self):
        #retrieve all the birds
        existing_birds = self.session.query(Bird).all()
        #delete the birds
        for old_bird in existing_birds:
            self.session.delete(old_bird)

        self.session.flush()
        #add new birds
        bird_data_path = os.path.join(self.app.root_path, "data", "unified_bird_data.json")
        bird_data = json.load(open(bird_data_path))
        birds=bird_data["data"]
        for bird in birds:
            
            stringed_list = ""
            for i, location in enumerate(bird["locations"]):
                if (i < len(bird["locations"])-1):
                    stringed_list = stringed_list + location + ';'
                else:
                    stringed_list = stringed_list + location 

            birdy = Bird(
                id=bird["id"].encode("utf-8", errors="ignore"), 
                name=bird["name"].encode("utf-8", errors="ignore"), 
                image=bird["image"].encode("utf-8", errors="ignore"),  
                description=bird["description"].encode("utf-8", errors="ignore"),  
                life_history=bird["lifeHistory"].encode("utf-8", errors="ignore"), 
                distribution_and_habitat=bird["distributionAndHabitat"].encode("utf-8", errors="ignore"), 
                status=bird["status"].encode("utf-8", errors="ignore"), 
                management_and_research_needs=bird["managementAndResearchNeeds"].encode("utf-8", errors="ignore"), 
                locations=stringed_list,
            )
            self.session.add(birdy)
            print(birdy.id)
        #save
        self.session.commit()

