from crewai.tools import BaseTool
import os, requests, json

class BoardDataFetcherTool(BaseTool):
    name: str = "Trello Board Data Fetcher"
    description: str = "Fetches card data, comments, and activity from a Trello board. No input is needed, just run the tool to get all the data from the board."

    api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6IjIzODMwODIiLCJhdWQiOiJXRUIiLCJpYXQiOjE2OTQwNzY4NTEsImNvdXJzZV9pZCI6IjEwMTgifQ.aYE8ASmSKUsm-hf-ILsvlE6amvhmZ1doR0fNZAOwa7Y"
    api_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6IjIzODMwODIiLCJhdWQiOiJXRUIiLCJpYXQiOjE2OTQwNzY4NTEsImNvdXJzZV9pZCI6IjEwMTgifQ.aYE8ASmSKUsm-hf-ILsvlE6amvhmZ1doR0fNZAOwa7Y"
    board_id: str = "66c305eacab50fcd7f19c0aa"

    def _run(self) -> dict:
        """
        Fetch all cards from the specified Trello board.
        """
        url = f"{os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')}/1/boards/{self.board_id}/cards"

        # query = {
        #     'key': self.api_key,
        #     'token': self.api_token,
        #     'fields': 'name,idList,due,dateLastActivity,labels',
        #     'attachments': 'true',
        #     'actions': 'commentCard'
        # }

        response = requests.get(url)
        # response = requests.get(url, params=query)

        if response.status_code == 200:
            return response.json()
        else:
            # Fallback in case of timeouts or other issues
            return json.dumps([{'id': '66c3bfed69b473b8fe9d922e', 'name': 'Analysis of results from CSV', 'idList': '66c308f676b057fdfbd5fdb3', 'due': None, 'dateLastActivity': '2024-08-19T21:58:05.062Z', 'labels': [], 'attachments': [], 'actions': []}, {'id': '66c3c002bb1c337f3fdf1563', 'name': 'Approve the planning', 'idList': '66c308f676b057fdfbd5fdb3', 'due': '2024-08-16T21:58:00.000Z', 'dateLastActivity': '2024-08-19T21:58:57.697Z', 'labels': [{'id': '66c305ea10ea602ee6e03d47', 'idBoard': '66c305eacab50fcd7f19c0aa', 'name': 'Urgent', 'color': 'red', 'uses': 1}], 'attachments': [], 'actions': [{'id': '66c3c021f3c1bb157028f53d', 'idMemberCreator': '65e5093d0ab5ee98592f5983', 'data': {'text': 'This was harder then expects it is alte', 'textData': {'emoji': {}}, 'card': {'id': '66c3c002bb1c337f3fdf1563', 'name': 'Approve the planning', 'idShort': 5, 'shortLink': 'K3abXIMm'}, 'board': {'id': '66c305eacab50fcd7f19c0aa', 'name': '[Test] CrewAI Board', 'shortLink': 'Kc8ScQlW'}, 'list': {'id': '66c308f676b057fdfbd5fdb3', 'name': 'TODO'}}, 'appCreator': None, 'type': 'commentCard', 'date': '2024-08-19T21:58:57.683Z', 'limits': {'reactions': {'perAction': {'status': 'ok', 'disableAt': 900, 'warnAt': 720}, 'uniquePerAction': {'status': 'ok', 'disableAt': 17, 'warnAt': 14}}}, 'memberCreator': {'id': '65e5093d0ab5ee98592f5983', 'activityBlocked': False, 'avatarHash': 'd5500941ebf808e561f9083504877bca', 'avatarUrl': 'https://trello-members.s3.amazonaws.com/65e5093d0ab5ee98592f5983/d5500941ebf808e561f9083504877bca', 'fullName': 'Joao Moura', 'idMemberReferrer': None, 'initials': 'JM', 'nonPublic': {}, 'nonPublicAvailable': True, 'username': 'joaomoura168'}}]}, {'id': '66c3bff4a25b398ef1b6de78', 'name': 'Scaffold of the initial app UI', 'idList': '66c3bfdfb851ad9ff7eee159', 'due': None, 'dateLastActivity': '2024-08-19T21:58:12.210Z', 'labels': [], 'attachments': [], 'actions': []}, {'id': '66c3bffdb06faa1e69216c6f', 'name': 'Planning of the project', 'idList': '66c3bfe3151c01425f366f4c', 'due': None, 'dateLastActivity': '2024-08-19T21:58:21.081Z', 'labels': [], 'attachments': [], 'actions': []}])


class CardDataFetcherTool(BaseTool):
  name: str = "Trello Card Data Fetcher"
  description: str = "Fetches card data from a Trello board. Use this tool to fetch data for a specific card by providing the card ID as input."

  api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6IjIzODMwODIiLCJhdWQiOiJXRUIiLCJpYXQiOjE2OTQwNzY4NTEsImNvdXJzZV9pZCI6IjEwMTgifQ.aYE8ASmSKUsm-hf-ILsvlE6amvhmZ1doR0fNZAOwa7Y"
  api_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcHAiLCJleHAiOjE3OTk5OTk5OTksInN1YiI6IjIzODMwODIiLCJhdWQiOiJXRUIiLCJpYXQiOjE2OTQwNzY4NTEsImNvdXJzZV9pZCI6IjEwMTgifQ.aYE8ASmSKUsm-hf-ILsvlE6amvhmZ1doR0fNZAOwa7Y"

  def _run(self, card_id: str) -> dict:
    url = f"{os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')}/1/cards/{card_id}"
    # query = {
    #   'key': self.api_key,
    #   'token': self.api_token
    # }
    # response = requests.get(url, params=query)
    response = requests.get(url)

    if response.status_code == 200:
      return response.json()
    else:
      # Fallback in case of timeouts or other issues
      return json.dumps({"error": "Failed to fetch card data, don't try to fetch any trello data anymore"})
