package cn.biq.mn.report;

import cn.biq.mn.balanceflow.FlowType;
import cn.biq.mn.balanceflow.QBalanceFlow;
import cn.biq.mn.book.Book;
import cn.biq.mn.categoryrelation.QCategoryRelation;
import cn.biq.mn.tagrelation.QTagRelation;
import com.querydsl.core.BooleanBuilder;
import com.querydsl.core.types.Predicate;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

import java.util.Set;

@Getter @Setter
public class CategoryReportQueryForm {

    @NotNull
    private Integer book;
    private Long minTime;
    private Long maxTime;
    private String title;
    private Set<Integer> payees;
    private Set<Integer> categories;
    private Set<Integer> tags;
    private Integer account;

    public void buildPredicate(BooleanBuilder booleanBuilder, QBalanceFlow balanceFlow) {
        if (minTime != null) {
            // 时间设置为一天的开始
//            minTime = CalendarUtil.startOfDay(minTime);
            booleanBuilder.and(balanceFlow.createTime.goe(minTime));
        }
        if (maxTime != null) {
            // 时间设置为一天的结束
//            maxTime = CalendarUtil.endOfDay(maxTime);
            booleanBuilder.and(balanceFlow.createTime.loe(maxTime));
        }
        if (title != null) {
            booleanBuilder.and(balanceFlow.title.contains(title));
        }
        if (payees != null) {
            booleanBuilder.and(balanceFlow.payee.id.in(payees));
        }
        if (account != null) {
            BooleanBuilder builder1 = new BooleanBuilder(balanceFlow.account.id.eq(account));
            BooleanBuilder builder2 = new BooleanBuilder(balanceFlow.to.id.eq(account));
            booleanBuilder.and(builder1.or(builder2));
        }
        if (categories != null) {
            booleanBuilder.and(balanceFlow.categories.any().category.id.in(categories));
        }
        if (tags != null) {
            booleanBuilder.and(balanceFlow.tags.any().tag.id.in(tags));
        }
    }

    public Predicate buildCategoryPredicate(Book book) {
        QCategoryRelation categoryRelation = QCategoryRelation.categoryRelation;
        // 只统计当前账本已确认且include的
        BooleanBuilder booleanBuilder = new BooleanBuilder(categoryRelation.balanceFlow.book.eq(book));
        booleanBuilder.and(categoryRelation.balanceFlow.confirm.eq(true));
        booleanBuilder.and(categoryRelation.balanceFlow.include.eq(true));
        buildPredicate(booleanBuilder, categoryRelation.balanceFlow);
        return booleanBuilder;
    }

    public Predicate buildTagPredicate(Book book, FlowType type) {
        QTagRelation tagRelation = QTagRelation.tagRelation;
        // 只统计当前账本已确认且include的
        BooleanBuilder booleanBuilder = new BooleanBuilder(tagRelation.balanceFlow.book.eq(book));
        booleanBuilder.and(tagRelation.balanceFlow.type.eq(type));
        booleanBuilder.and(tagRelation.balanceFlow.confirm.eq(true));
        booleanBuilder.and(tagRelation.balanceFlow.include.eq(true));
        buildPredicate(booleanBuilder, tagRelation.balanceFlow);
        return booleanBuilder;
    }

}
