package cn.biq.mn.group;

import cn.biq.mn.base.BaseService;
import cn.biq.mn.base.IdAndNameMapper;
import cn.biq.mn.bean.ApplicationScopeBean;
import cn.biq.mn.book.BookService;
import cn.biq.mn.book.tpl.BookTemplate;
import cn.biq.mn.exception.FailureMessageException;
import cn.biq.mn.exception.ItemNotFoundException;
import cn.biq.mn.balanceflow.BalanceFlowRepository;
import cn.biq.mn.base.BaseEntityRepository;
import cn.biq.mn.book.Book;
import cn.biq.mn.book.BookRepository;
import cn.biq.mn.category.CategoryRepository;
import cn.biq.mn.currency.CurrencyService;
import cn.biq.mn.payee.PayeeRepository;
import cn.biq.mn.tag.TagRepository;
import cn.biq.mn.user.*;
import cn.biq.mn.utils.EnumUtils;
import cn.biq.mn.utils.Limitation;
import cn.biq.mn.utils.SessionUtil;
import com.querydsl.core.BooleanBuilder;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class GroupService {

    private final SessionUtil sessionUtil;
    private final GroupRepository groupRepository;
    private final BookRepository bookRepository;
    private final UserGroupRelationRepository userGroupRelationRepository;
    private final EnumUtils enumUtils;
    private final CurrencyService currencyService;
    private final BalanceFlowRepository balanceFlowRepository;
    private final CategoryRepository categoryRepository;
    private final TagRepository tagRepository;
    private final PayeeRepository payeeRepository;
    private final UserRepository userRepository;
    private final BaseEntityRepository baseEntityRepository;
    private final ApplicationScopeBean applicationScopeBean;
    private final BookService bookService;
    private final BaseService baseService;

    @Transactional(readOnly = true)
    public Page<GroupDetails> query(Pageable page) {
        User user = sessionUtil.getCurrentUser();
        QGroup qGroup = QGroup.group;
        BooleanBuilder booleanBuilder = new BooleanBuilder();
        booleanBuilder.and(qGroup.relations.any().user.eq(user));
        Page<Group> entityPage = groupRepository.findAll(booleanBuilder, page);
        return entityPage.map(group -> {
            var details = GroupMapper.toDetails(group);
            var relation = userGroupRelationRepository.findByGroupAndUser(group, user).get();
            details.setRoleId(relation.getRole());
            details.setRole(enumUtils.translateRoleType(relation.getRole()));
            details.setCurrent(details.getId().equals(sessionUtil.getCurrentGroup().getId()));
            details.setDefaultBook(IdAndNameMapper.toDetails(group.getDefaultBook()));
            return details;
        });
    }

    public boolean add(GroupAddForm form) {
        User user = sessionUtil.getCurrentUser();
        if (groupRepository.countByCreator(user) >= Limitation.group_max_count) {
            throw new FailureMessageException("group.max.count");
        }
        currencyService.checkCode(form.getDefaultCurrencyCode());
        Group group = new Group();
        group.setName(form.getName());
        group.setNotes(form.getNotes());
        group.setDefaultCurrencyCode(form.getDefaultCurrencyCode());
        group.setCreator(user);
        groupRepository.save(group);

        // 生成一个账本
        List<BookTemplate> bookTplList = applicationScopeBean.getBookTplList();
        Optional<BookTemplate> bookTemplateOptional = bookTplList.stream()
                .filter(bookTemplate -> bookTemplate.getId().equals(form.getTemplateId()))
                .findFirst();
        if (bookTemplateOptional.isPresent()) {
            BookTemplate bookTemplate = bookTemplateOptional.get();
            Book book = new Book();
            book.setName(bookTemplate.getName());
            bookService.setBookByBookTemplate(bookTemplate, group, book);
            group.setDefaultBook(book);
            groupRepository.save(group);
            UserGroupRelation relation = new UserGroupRelation(user, group, 1);
            userGroupRelationRepository.save(relation);
            return true;
        } else {
            throw new ItemNotFoundException();
        }
    }

    private void checkRole(Group group) {
        User user = sessionUtil.getCurrentUser();
        var relationOptional = userGroupRelationRepository.findByGroupAndUser(group, user);
        if (relationOptional.isEmpty()) {
            throw new FailureMessageException("group.update.auth.error");
        }
        var relation = relationOptional.get();
        if (relation.getRole() != 1) {
            throw new FailureMessageException("group.update.auth.error");
        }
    }

    private void checkInvite(Group group) {
        User user = sessionUtil.getCurrentUser();
        var relationOptional = userGroupRelationRepository.findByGroupAndUser(group, user);
        if (relationOptional.isEmpty()) {
            throw new FailureMessageException("group.update.auth.error");
        }
        var relation = relationOptional.get();
        if (relation.getRole() != 4) {
            throw new FailureMessageException("group.update.auth.error");
        }
    }

    public boolean update(Integer id, GroupUpdateForm form) {
        currencyService.checkCode(form.getDefaultCurrencyCode());
        Group entity = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkRole(entity);
        entity.setName(form.getName());
        entity.setNotes(form.getNotes());
        entity.setDefaultCurrencyCode(form.getDefaultCurrencyCode());
        Book book = baseService.getBookInGroup(form.getDefaultBookId());
        if (!book.getEnable()) {
            throw new ItemNotFoundException();
        }
        entity.setDefaultBook(book);
        groupRepository.save(entity);
        // 更新的是当前的默认组，则需要更新CurrentSession里面的对象
        if (entity.getId().equals(sessionUtil.getCurrentGroup().getId())) {
            sessionUtil.setCurrentGroup(entity);
        }
        return true;
    }

    public boolean remove(Integer id) {
        Group entity = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkRole(entity);
        if (entity.getId().equals(sessionUtil.getCurrentGroup().getId())) {
            throw new FailureMessageException("group.update.auth.error");
        }
        // 如果只剩一个自己创建的组，则无法删除，用于回退
        var relations = userGroupRelationRepository.findByUserAndRole(sessionUtil.getCurrentUser(), 1);
        if (relations.size() <= 1) {
            throw new FailureMessageException("group.delete.size.error");
        }

        List<Book> books = bookRepository.findAllByGroup(entity);
        books.forEach(book -> {
            if (balanceFlowRepository.existsByBook(book)) {
                throw new FailureMessageException("group.delete.has.flow");
            }
            categoryRepository.deleteByBook(book);
            payeeRepository.deleteByBook(book);
            tagRepository.deleteByBook(book);
            bookRepository.delete(book);
        });
        userGroupRelationRepository.deleteByGroup(entity);
        groupRepository.delete(entity);
        return true;
    }

    public boolean inviteUser(Integer id, InviteUserForm form) {
        User user = userRepository.findOneByUsername(form.getUsername()).orElseThrow(() -> new FailureMessageException("invite.user.not.exists"));
        Group group = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkRole(group);
        var relationOptional = userGroupRelationRepository.findByGroupAndUser(group, user);
        if (relationOptional.isPresent()) {
            throw new FailureMessageException("invite.user.has.role");
        }
        var relation = new UserGroupRelation(user, group, 4);
        baseEntityRepository.save(relation);
        return true;
    }

    public boolean removeUser(Integer groupId, Integer userId) {
        Group group = groupRepository.findById(groupId).orElseThrow(ItemNotFoundException::new);
        // 组的所有者才能删除用户
        checkRole(group);
        User user = userRepository.findById(userId).orElseThrow(ItemNotFoundException::new);
        var relation = userGroupRelationRepository.findByGroupAndUser(group, user).orElseThrow(ItemNotFoundException::new);
        // 不能删除自己
        if (relation.getRole() == 1) {
            throw new FailureMessageException("group.remove.user.self");
        }
        // 如果这个组是他之前的默认组
        if (group.getId().equals(user.getDefaultGroup().getId())) {
            // 应该最少有一条是他创建的组
            var relations = userGroupRelationRepository.findByUserAndRole(user, 1);
            Group newDefaultGroup = relations.get(0).getGroup();
            user.setDefaultGroup(newDefaultGroup);
            user.setDefaultBook(newDefaultGroup.getDefaultBook());
            userRepository.save(user);
            // TODO 如果用户处于登录状态？
        }
        baseEntityRepository.delete(relation);
        return true;
    }

    public boolean agreeInvite(Integer id) {
        Group group = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkInvite(group);
        User user = sessionUtil.getCurrentUser();
        var relationOptional = userGroupRelationRepository.findByGroupAndUser(group, user);
        var relation = relationOptional.get();
        relation.setRole(2);
        baseEntityRepository.save(relation);
        return true;
    }

    public boolean rejectInvite(Integer id) {
        Group group = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkInvite(group);
        User user = sessionUtil.getCurrentUser();
        var relationOptional = userGroupRelationRepository.findByGroupAndUser(group, user);
        var relation = relationOptional.get();
        baseEntityRepository.delete(relation);
        return true;
    }

    public List<GroupUserDetails> getUsers(Integer id) {
        Group group = groupRepository.findById(id).orElseThrow(ItemNotFoundException::new);
        checkRole(group);
        QUserGroupRelation qUserGroupRelation = QUserGroupRelation.userGroupRelation;
        BooleanBuilder booleanBuilder = new BooleanBuilder();
        booleanBuilder.and(qUserGroupRelation.group.eq(group));
        List<UserGroupRelation> relations = userGroupRelationRepository.findAll(booleanBuilder);
        List<GroupUserDetails> userList = new ArrayList<>();
        for(var relation : relations) {
            User user = relation.getUser();
            var groupUser = new GroupUserDetails();
            groupUser.setId(user.getId());
            groupUser.setUsername(user.getUsername());
            groupUser.setNickName(user.getNickName());
            groupUser.setRole(enumUtils.translateRoleType(relation.getRole()));
            groupUser.setRoleId(relation.getRole());
            userList.add(groupUser);
        }
        return userList;
    }

}
