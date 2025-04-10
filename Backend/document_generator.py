def generate_document(data):
    # data = {'type': 'NDA', 'partyA': 'Alice', 'partyB': 'Bob'}
    if data['type'] == 'NDA':
        return f"This NDA is between {data['partyA']} and {data['partyB']}..."
    return "Unsupported document type"
