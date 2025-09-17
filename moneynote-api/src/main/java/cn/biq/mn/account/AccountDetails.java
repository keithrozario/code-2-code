package cn.biq.mn.account;

import cn.biq.mn.base.IdAndNameDetails;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Getter @Setter
public class AccountDetails extends IdAndNameDetails {

    private AccountType type;
    private String typeName;
    private String no;
    private BigDecimal balance;
    private BigDecimal convertedBalance;
    private BigDecimal rate;
    private Boolean enable;
    private Boolean include;
    private Boolean canExpense;
    private Boolean canIncome;
    private Boolean canTransferFrom;
    private Boolean canTransferTo;
    private String notes;
    private String currencyCode;

    private BigDecimal creditLimit;
    private Integer billDay;

    private BigDecimal apr;
    private Long asOfDate;

    private Integer sort;

    public BigDecimal getRemainLimit() {
        if (creditLimit == null) return null;
        return creditLimit.add(getBalance());
    }

    @Override
    public String getLabel() {
        return getName();
    }
}
