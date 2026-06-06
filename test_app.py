from app import app

# 1. Test 1: Verify the App Header is present and contains correct text
def test_header_present():
    # Dig into the app's layout tree to find the H1 element
    layout = app.layout
    main_container = layout.children[0]
    header_section = main_container.children[0]
    h1_element = header_section.children[0]
    
    assert h1_element is not None
    assert h1_element.children == "Soul Foods: Pink Morsel Regional Sales Dashboard"

# 2. Test 2: Verify the Visualisation (Graph) component exists in the layout
def test_visualization_present():
    layout = app.layout
    main_container = layout.children[0]
    
    # Locate the container wrapper holding the Graph component
    graph_wrapper = main_container.children[2]
    graph_component = graph_wrapper.children[0]
    
    assert graph_component is not None
    assert graph_component.id == "sales-line-chart"

# 3. Test 3: Verify the Region Picker (Radio Items) element exists in the layout
def test_region_picker_present():
    layout = app.layout
    main_container = layout.children[0]
    
    # Locate the Control Filter block holding the RadioItems component
    filter_card = main_container.children[1]
    radio_items_component = filter_card.children[1]
    
    assert radio_items_component is not None
    assert radio_items_component.id == "region-filter"