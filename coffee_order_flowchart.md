# Coffee Order Process Flowchart

This flowchart details the process for ordering a coffee, from choosing a size to sending the order to the barista.

```mermaid
flowchart TD
    Start([Customer Starts Order]) --> ChooseSize[Choose Size]
    ChooseSize --> SizeOptions{Select Size}
    SizeOptions -->|Small| SelectType1[Select Coffee Type]
    SizeOptions -->|Medium| SelectType2[Select Coffee Type]
    SizeOptions -->|Large| SelectType3[Select Coffee Type]

    SelectType1 --> TypeChoice1{Latte or Cappuccino?}
    SelectType2 --> TypeChoice2{Latte or Cappuccino?}
    SelectType3 --> TypeChoice3{Latte or Cappuccino?}

    TypeChoice1 -->|Latte| AddFlavor1[Add Optional Flavor Shots]
    TypeChoice1 -->|Cappuccino| AddFlavor2[Add Optional Flavor Shots]
    TypeChoice2 -->|Latte| AddFlavor3[Add Optional Flavor Shots]
    TypeChoice2 -->|Cappuccino| AddFlavor4[Add Optional Flavor Shots]
    TypeChoice3 -->|Latte| AddFlavor5[Add Optional Flavor Shots]
    TypeChoice3 -->|Cappuccino| AddFlavor6[Add Optional Flavor Shots]

    AddFlavor1 --> FlavorChoice1{Add Flavor?}
    AddFlavor2 --> FlavorChoice2{Add Flavor?}
    AddFlavor3 --> FlavorChoice3{Add Flavor?}
    AddFlavor4 --> FlavorChoice4{Add Flavor?}
    AddFlavor5 --> FlavorChoice5{Add Flavor?}
    AddFlavor6 --> FlavorChoice6{Add Flavor?}

    FlavorChoice1 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder1[Send to Barista]
    FlavorChoice1 -->|No| SendOrder1
    FlavorChoice2 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder2[Send to Barista]
    FlavorChoice2 -->|No| SendOrder2
    FlavorChoice3 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder3[Send to Barista]
    FlavorChoice3 -->|No| SendOrder3
    FlavorChoice4 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder4[Send to Barista]
    FlavorChoice4 -->|No| SendOrder4
    FlavorChoice5 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder5[Send to Barista]
    FlavorChoice5 -->|No| SendOrder5
    FlavorChoice6 -->|Yes - Vanilla/Caramel/Hazelnut| SendOrder6[Send to Barista]
    FlavorChoice6 -->|No| SendOrder6

    SendOrder1 --> End([Order Complete])
    SendOrder2 --> End
    SendOrder3 --> End
    SendOrder4 --> End
    SendOrder5 --> End
    SendOrder6 --> End
```

## Process Steps

1. **Choose Size**: Customer selects Small, Medium, or Large
2. **Select Type**: Customer chooses between Latte or Cappuccino
3. **Add Flavor Shots**: Customer can optionally add flavor shots (Vanilla, Caramel, or Hazelnut)
4. **Send to Barista**: Order is finalized and sent to the barista
5. **Order Complete**: Process ends
