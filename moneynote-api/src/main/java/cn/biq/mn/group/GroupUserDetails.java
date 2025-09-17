package cn.biq.mn.group;

import cn.biq.mn.base.BaseDetails;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class GroupUserDetails extends BaseDetails {

    private String username;
    private String nickName;
    private String role;
    private Integer roleId;

}
