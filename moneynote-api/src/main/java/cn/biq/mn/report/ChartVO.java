package cn.biq.mn.report;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter @Setter
public class ChartVO {

    private String x;
    private BigDecimal y;
    private BigDecimal percent;

}
